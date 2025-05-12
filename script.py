import time
import concurrent.futures
from pathlib import Path
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup

def extract_pdf_text(file_path):
    try:
        start = time.time()
        text = extract_text(file_path)
        duration = time.time() - start
        return text, duration, None
    except Exception as e:
        return None, 0, str(e)

def extract_html_text(file_path):
    try:
        start = time.time()
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text()
        duration = time.time() - start
        return text, duration, None
    except Exception as e:
        return None, 0, str(e)

def process_file(file_path, output_dir):
    ext = file_path.suffix.lower()
    if ext == '.pdf':
        text, duration, error = extract_pdf_text(file_path)
    elif ext == '.html':
        text, duration, error = extract_html_text(file_path)
    else:
        return ext, False, 0

    if text and not error:
        output_file = output_dir / (file_path.stem + '.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        return ext, True, duration
    return ext, False, 0

def main():
    input_dir = Path('Documentos')
    output_dir = Path('texts')
    report_dir = Path('relatorio')
    
    output_dir.mkdir(exist_ok=True)
    report_dir.mkdir(exist_ok=True)
    
    pdf_success = html_success = pdf_error = html_error = 0
    pdf_time = html_time = 0
    pdf_count = html_count = 0

    start_time = time.time()

    files = list(input_dir.glob('*.*'))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, f, output_dir) for f in files]
        for future in concurrent.futures.as_completed(futures):
            ext, success, duration = future.result()
            if ext == '.pdf':
                pdf_count += 1
                if success:
                    pdf_success += 1
                    pdf_time += duration
                else:
                    pdf_error += 1
            elif ext == '.html':
                html_count += 1
                if success:
                    html_success += 1
                    html_time += duration
                else:
                    html_error += 1

    total_time = time.time() - start_time
    avg_pdf_time = pdf_time / pdf_success if pdf_success else 0
    avg_html_time = html_time / html_success if html_success else 0

    report = f"""
    Relatório de Processamento
    --------------------------
    Tempo total: {total_time:.2f}s

    PDFs processados com sucesso: {pdf_success}
    PDFs com erro: {pdf_error}
    HTMLs processados com sucesso: {html_success}
    HTMLs com erro: {html_error}

    Tempo médio por PDF: {avg_pdf_time:.2f}s
    Tempo médio por HTML: {avg_html_time:.2f}s
    """
    print(report)

    with open(report_dir / 'relatorio.txt', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == '__main__':
    main()