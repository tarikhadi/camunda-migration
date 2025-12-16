#!/usr/bin/env python3
"""
Indexador Avançado com Suporte a Imagens
==========================================
Processa PDFs, extrai texto e imagens, cria embeddings e banco vetorial
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
import hashlib

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from pypdf import PdfReader
import fitz  # PyMuPDF para extração de imagens reais
from PIL import Image
import io

from config import GOOGLE_API_KEY
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


class AdvancedPDFProcessor:
    """Processador avançado de PDFs com extração de imagens"""
    
    def __init__(self, docs_path: str):
        self.docs_path = Path(docs_path)
        self.images_dir = Path("extracted_images")
        self.images_dir.mkdir(exist_ok=True)
        self.image_metadata = {}
        
    def extract_images_from_pdf(self, pdf_path: Path) -> Dict[int, List[str]]:
        """Extrai IMAGENS REAIS de um PDF (diagramas, gráficos, etc) e salva localmente"""
        console.print(f"  [yellow]📷[/yellow] Extraindo imagens REAIS de {pdf_path.name}...")
        
        images_by_page = {}
        total_images = 0
        
        try:
            # Abre PDF com PyMuPDF
            pdf_document = fitz.open(str(pdf_path))
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                page_number = page_num + 1  # 1-indexed
                
                # Obtém lista de imagens na página
                image_list = page.get_images(full=True)
                
                if not image_list:
                    continue  # Sem imagens nesta página
                
                if page_number not in images_by_page:
                    images_by_page[page_number] = []
                
                # Extrai cada imagem
                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]  # Referência da imagem
                        
                        # Extrai a imagem
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # Nome do arquivo
                        img_filename = f"{pdf_path.stem}_p{page_number}_img{img_index}.{image_ext}"
                        img_path = self.images_dir / img_filename
                        
                        # Salva imagem
                        with open(img_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        
                        # Converte para PNG se necessário (para consistência)
                        if image_ext != "png":
                            img = Image.open(img_path)
                            png_filename = f"{pdf_path.stem}_p{page_number}_img{img_index}.png"
                            png_path = self.images_dir / png_filename
                            img.save(png_path, "PNG")
                            img_path.unlink()  # Remove original
                            img_path = png_path
                            img_filename = png_filename
                        
                        images_by_page[page_number].append(str(img_path))
                        total_images += 1
                        
                        # Armazena metadata
                        self.image_metadata[img_filename] = {
                            'document': pdf_path.stem,
                            'page': page_number,
                            'path': str(img_path),
                            'index': img_index
                        }
                        
                    except Exception as e:
                        console.print(f"    [dim]⚠️  Erro ao extrair imagem {img_index} da página {page_number}: {e}[/dim]")
                        continue
            
            pdf_document.close()
            
            if total_images > 0:
                console.print(f"    ✓ {total_images} imagens REAIS extraídas de {len(images_by_page)} páginas")
            else:
                console.print(f"    [dim]⚠️  Nenhuma imagem encontrada neste PDF[/dim]")
            
        except Exception as e:
            console.print(f"    [red]✗[/red] Erro ao processar PDF: {e}")
        
        return images_by_page
    
    def process_pdf(self, pdf_path: Path) -> Tuple[List[Document], Dict]:
        """Processa um PDF: extrai texto, metadados e imagens"""
        console.print(f"\n[cyan]📄 Processando:[/cyan] {pdf_path.name}")
        
        documents = []
        
        try:
            # Extrai imagens
            images_by_page = self.extract_images_from_pdf(pdf_path)
            
            # Lê PDF
            reader = PdfReader(str(pdf_path))
            
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                
                if text.strip():
                    # Identifica se há imagens nesta página
                    page_images = images_by_page.get(page_num, [])
                    
                    doc = Document(
                        page_content=text,
                        metadata={
                            'source': pdf_path.stem,
                            'page': page_num,
                            'total_pages': len(reader.pages),
                            'has_images': len(page_images) > 0,
                            'images': json.dumps(page_images),  # ← Converte lista para JSON string
                            'section': self._identify_section(text)
                        }
                    )
                    documents.append(doc)
            
            console.print(f"  [green]✓[/green] {len(documents)} páginas processadas")
            
        except Exception as e:
            console.print(f"  [red]✗[/red] Erro: {e}")
        
        return documents, images_by_page
    
    def _identify_section(self, text: str) -> str:
        """Identifica a seção do documento baseado no texto"""
        text_lower = text.lower()
        
        # Palavras-chave para identificar seções
        sections = {
            'introduction': ['introduction', 'introdução', 'overview'],
            'architecture': ['architecture', 'arquitetura', 'design'],
            'migration': ['migration', 'migração', 'migrating'],
            'code_conversion': ['code conversion', 'conversão de código', 'converting code'],
            'data_migration': ['data migr', 'migração de dados', 'data migrator'],
            'tools': ['tools', 'ferramentas', 'tooling'],
            'best_practices': ['best practices', 'boas práticas', 'recommendations'],
            'concepts': ['concept', 'conceito', 'fundamental'],
        }
        
        for section_name, keywords in sections.items():
            if any(keyword in text_lower for keyword in keywords):
                return section_name
        
        return 'general'


class AdvancedIndexer:
    """Indexador avançado com embeddings Google e ChromaDB"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )
        self.vectorstore = None
        self.processor = AdvancedPDFProcessor("documentação_migracao_camunda")
        
    def create_chunks(self, documents: List[Document]) -> List[Document]:
        """Cria chunks dos documentos com overlap"""
        console.print("\n[cyan]✂️  Criando chunks...[/cyan]")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Tamanho do chunk
            chunk_overlap=200,  # Overlap para manter contexto
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        
        # Adiciona ID único a cada chunk
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = f"chunk_{i}"
            chunk.metadata['chunk_index'] = i
        
        console.print(f"  [green]✓[/green] {len(chunks)} chunks criados")
        return chunks
    
    def build_vectorstore(self, chunks: List[Document]) -> Chroma:
        """Cria banco vetorial com ChromaDB"""
        console.print("\n[cyan]🗄️  Criando banco vetorial...[/cyan]")
        
        persist_directory = "./chroma_db"
        
        try:
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=persist_directory,
                collection_name="camunda_migration"
            )
            
            console.print(f"  [green]✓[/green] Banco vetorial criado em {persist_directory}")
            console.print(f"  [green]✓[/green] {len(chunks)} chunks indexados")
            
            return vectorstore
            
        except Exception as e:
            console.print(f"  [red]✗[/red] Erro: {e}")
            raise
    
    def index_all_documents(self):
        """Indexa todos os PDFs da documentação"""
        console.print("\n[bold cyan]🚀 Iniciando Indexação Avançada[/bold cyan]")
        console.print("="*70 + "\n")
        
        pdf_files = list(self.processor.docs_path.glob("*.pdf"))
        
        if not pdf_files:
            console.print("[red]❌ Nenhum PDF encontrado![/red]")
            return
        
        console.print(f"📚 Encontrados {len(pdf_files)} documentos\n")
        
        all_documents = []
        all_images_metadata = {}
        
        # Processa cada PDF
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            
            task = progress.add_task("Processando PDFs...", total=len(pdf_files))
            
            for pdf_file in pdf_files:
                docs, images = self.processor.process_pdf(pdf_file)
                all_documents.extend(docs)
                all_images_metadata.update(self.processor.image_metadata)
                progress.advance(task)
        
        # Salva metadata de imagens
        with open("image_metadata.json", "w") as f:
            json.dump(all_images_metadata, f, indent=2)
        
        console.print(f"\n[green]✓[/green] Total: {len(all_documents)} documentos processados")
        
        # Cria chunks
        chunks = self.create_chunks(all_documents)
        
        # Cria embeddings e vectorstore
        self.vectorstore = self.build_vectorstore(chunks)
        
        console.print("\n" + "="*70)
        console.print("[bold green]✅ INDEXAÇÃO CONCLUÍDA COM SUCESSO![/bold green]")
        console.print("="*70 + "\n")
        
        # Estatísticas
        self._print_statistics(all_documents, chunks, all_images_metadata)
    
    def _print_statistics(self, documents, chunks, images_metadata):
        """Imprime estatísticas da indexação"""
        console.print("[bold]📊 Estatísticas:[/bold]\n")
        
        # Documentos
        doc_sources = set(doc.metadata['source'] for doc in documents)
        console.print(f"  📄 Documentos únicos: {len(doc_sources)}")
        console.print(f"  📃 Total de páginas: {len(documents)}")
        console.print(f"  ✂️  Total de chunks: {len(chunks)}")
        
        # Imagens
        console.print(f"  📷 Total de imagens: {len(images_metadata)}")
        
        chunks_with_images = sum(1 for chunk in chunks if chunk.metadata.get('has_images'))
        console.print(f"  🖼️  Chunks com imagens: {chunks_with_images}")
        
        # Seções
        sections = {}
        for doc in documents:
            section = doc.metadata.get('section', 'unknown')
            sections[section] = sections.get(section, 0) + 1
        
        console.print(f"\n  📑 Páginas por seção:")
        for section, count in sorted(sections.items(), key=lambda x: x[1], reverse=True):
            console.print(f"     • {section}: {count}")
        
        console.print()


def main():
    """Função principal"""
    
    # Verifica API key
    if not GOOGLE_API_KEY:
        console.print("[red]❌ GOOGLE_API_KEY não configurada no config.py![/red]")
        return
    
    # Cria indexador
    indexer = AdvancedIndexer(GOOGLE_API_KEY)
    
    # Executa indexação
    try:
        indexer.index_all_documents()
        
        console.print("[bold green]🎉 Pronto! Execute o chatbot avançado:[/bold green]")
        console.print("[cyan]   streamlit run chatbot_advanced.py[/cyan]\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Erro durante indexação: {e}[/bold red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

