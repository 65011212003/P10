"""Module for extracting images from PDF and DOCX files."""

import io
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image


class ImageData:
    """Container for image data."""
    
    def __init__(self, image: Image.Image, page_num: Optional[int] = None, description: str = ""):
        """Initialize image data."""
        self.image = image
        self.page_num = page_num
        self.description = description
        self.width, self.height = image.size
    
    def save(self, output_path: str) -> None:
        """Save image to file."""
        self.image.save(output_path)
    
    def to_bytes(self, format: str = 'PNG') -> bytes:
        """Convert image to bytes."""
        buffer = io.BytesIO()
        self.image.save(buffer, format=format)
        return buffer.getvalue()


def extract_images_from_pdf(file_path: str, max_images: int = 20) -> List[ImageData]:
    """
    Extract images from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        max_images: Maximum number of images to extract
        
    Returns:
        List of ImageData objects
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf package required for PDF image extraction")
    
    images = []
    
    try:
        reader = PdfReader(file_path)
        
        for page_num, page in enumerate(reader.pages, start=1):
            if len(images) >= max_images:
                break
            
            if '/XObject' in page['/Resources']:
                xobjects = page['/Resources']['/XObject'].get_object()
                
                for obj_name in xobjects:
                    if len(images) >= max_images:
                        break
                    
                    obj = xobjects[obj_name]
                    
                    if obj['/Subtype'] == '/Image':
                        try:
                            # Get image data
                            if '/Filter' in obj:
                                filter_type = obj['/Filter']
                                if filter_type == '/DCTDecode':  # JPEG
                                    img_data = obj._data
                                    img = Image.open(io.BytesIO(img_data))
                                elif filter_type == '/FlateDecode':  # PNG
                                    img_data = obj._data
                                    width = obj['/Width']
                                    height = obj['/Height']
                                    
                                    # Handle different color spaces
                                    if '/ColorSpace' in obj:
                                        color_space = obj['/ColorSpace']
                                        if color_space == '/DeviceRGB':
                                            mode = 'RGB'
                                        elif color_space == '/DeviceGray':
                                            mode = 'L'
                                        else:
                                            mode = 'RGB'
                                    else:
                                        mode = 'RGB'
                                    
                                    img = Image.frombytes(mode, (width, height), img_data)
                                else:
                                    continue
                            else:
                                continue
                            
                            # Filter out very small images (likely icons/logos)
                            if img.width >= 100 and img.height >= 100:
                                images.append(ImageData(
                                    image=img,
                                    page_num=page_num,
                                    description=f"Image from page {page_num}"
                                ))
                        except Exception:
                            # Skip problematic images
                            continue
    
    except Exception as e:
        # Return empty list if extraction fails
        pass
    
    return images


def extract_images_from_docx(file_path: str, max_images: int = 20) -> List[ImageData]:
    """
    Extract images from a DOCX file.
    
    Args:
        file_path: Path to the DOCX file
        max_images: Maximum number of images to extract
        
    Returns:
        List of ImageData objects
    """
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx package required for DOCX image extraction")
    
    images = []
    
    try:
        doc = Document(file_path)
        
        # Extract inline images from relationships
        for rel in doc.part.rels.values():
            if len(images) >= max_images:
                break
            
            if "image" in rel.target_ref:
                try:
                    img_data = rel.target_part.blob
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Filter out very small images
                    if img.width >= 100 and img.height >= 100:
                        images.append(ImageData(
                            image=img,
                            description="Image from document"
                        ))
                except Exception:
                    # Skip problematic images
                    continue
    
    except Exception as e:
        # Return empty list if extraction fails
        pass
    
    return images


def extract_images(file_path: str, max_images: int = 20) -> List[ImageData]:
    """
    Extract images from supported file types.
    
    Args:
        file_path: Path to the file
        max_images: Maximum number of images to extract
        
    Returns:
        List of ImageData objects
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == '.pdf':
        return extract_images_from_pdf(file_path, max_images)
    elif ext == '.docx':
        return extract_images_from_docx(file_path, max_images)
    else:
        return []


def get_image_statistics(images: List[ImageData]) -> Dict[str, Any]:
    """
    Get statistics about extracted images.
    
    Args:
        images: List of ImageData objects
        
    Returns:
        Dictionary with image statistics
    """
    if not images:
        return {
            'count': 0,
            'total_size_mb': 0,
            'avg_width': 0,
            'avg_height': 0,
        }
    
    total_width = sum(img.width for img in images)
    total_height = sum(img.height for img in images)
    
    # Estimate size in MB
    total_size_mb = sum(len(img.to_bytes()) for img in images) / (1024 * 1024)
    
    return {
        'count': len(images),
        'total_size_mb': round(total_size_mb, 2),
        'avg_width': int(total_width / len(images)),
        'avg_height': int(total_height / len(images)),
    }
