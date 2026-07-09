from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os
import logging


def load_pdf(uploaded_file):
    """
    Reads an uploaded PDF file
    and returns its contents.
    """
    temp_path = None
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        # Read the PDF
        loader = PyPDFLoader(temp_path)
        documents = loader.load()
        return documents
    except Exception as e:
        logging.error(f"Error parsing PDF file {uploaded_file.name}: {str(e)}", exc_info=True)
        raise RuntimeError("Unable to process the uploaded PDF.")
    finally:
        # Clean up temporary file safely
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as cleanup_err:
                logging.warning(f"Failed to clean up temp file {temp_path}: {str(cleanup_err)}")