from .pipeline.solver import process_document


async def process_pdf(file_bytes: bytes):

    results = process_document(file_bytes)

    return {
        "meta": {
            "is_complex": len(results) > 3
        },
        "results": results
    }
