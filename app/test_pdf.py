
from app.pdf_loader import load_pdf
result = load_pdf('data/uploads/user_manuel.pdf')
print('Filename:', result['filename'])
print('Chunks:', result['num_chunks'])
print('Apercu:', result['chunks'][0][:200])