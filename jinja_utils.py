from jinja2 import Environment, FileSystemLoader, Template
import os

def convert_text_to_html(text: str) -> str:
    """일반 텍스트를 HTML 형식으로 변환합니다."""
    # 기본 스타일 정의
    base_style = 'style="font-size: 10pt; font-family: 맑은 고딕; font-style: normal; font-variant-ligatures: normal; ' \
                'font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; ' \
                'text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; ' \
                'white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; ' \
                'text-decoration-color: initial; color: rgb(51, 51, 51)"'
    
    # 제목 스타일 정의
    title_style = 'style="font-size: 12px; font-family: 맑은 고딕; font-style: normal; font-variant-ligatures: normal; ' \
                 'font-variant-caps: normal; font-weight: bold; letter-spacing: normal; orphans: 2; text-align: center; ' \
                 'text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; ' \
                 'white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; ' \
                 'text-decoration-color: initial; color: #0033CC"'
    
    # 줄바꿈을 <br>과 들여쓰기로 변환
    paragraphs = text.split('\n\n')  # 빈 줄로 문단 구분
    
    formatted_paragraphs = []
    for i, p in enumerate(paragraphs):
        # 각 줄을 <br>로 연결
        lines = p.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():  # 빈 줄이 아닌 경우
                # 들여쓰기가 필요한 경우 &nbsp; 추가
                if line.startswith(' '):
                    line = '&nbsp;' * (len(line) - len(line.lstrip())) + line.lstrip()
                
                # 첫 번째 문단의 첫 줄은 제목 스타일 적용
                if i == 0 and not formatted_lines:
                    # 제이씨현시스템㈜ 부분과 나머지 부분 분리
                    if "제이씨현시스템" in line:
                        company_part = line[:line.find("제이씨현시스템") + len("제이씨현시스템㈜")]
                        rest_part = line[line.find("제이씨현시스템") + len("제이씨현시스템㈜"):]
                        formatted_lines.append(
                            f'<font size="2" color="#0033CC" style="font-family: 맑은 고딕;"><b>{company_part}</b></font>'
                            f'<span {title_style}>{rest_part}</span><br>\n'
                        )
                    else:
                        formatted_lines.append(f'<span {title_style}>{line}</span><br>\n')
                else:
                    # 나머지 텍스트는 기본 스타일 적용
                    formatted_lines.append(f'<span lang="EN-US" {base_style}>{line}</span><br>\n')
        
        # 문단을 합치기
        if formatted_lines:
            paragraph = ''.join(formatted_lines)
            formatted_paragraphs.append(paragraph)
            # 문단 사이에 빈 줄 추가
            formatted_paragraphs.append('<br>\n')
    
    # 모든 문단을 합치고 마지막 빈 줄 제거
    result = ''.join(formatted_paragraphs)
    if result.endswith('<br>\n'):
        result = result[:-5]
    
    return result

def generate_press_release_html(title: str, body_text: str) -> str:
    """
    - title: 문서의 <title> 태그 및 제목 표시용
    - body_text: 보도자료 본문(HTML 태그 포함 가능)
    return: 최종적으로 합쳐진 HTML 문자열
    """
    # 템플릿 로더 설정 (현재 디렉토리 기준 templates 폴더)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, 'templates')

    env = Environment(loader=FileSystemLoader(templates_dir))

    # press_release_template.html 읽기
    template = env.get_template('press_release_template.html')

    # 일반 텍스트를 HTML로 변환
    body_html = convert_text_to_html(body_text)
    
    # 템플릿 렌더링
    rendered_html = template.render(
        title=title,
        body_content=body_html
    )

    return rendered_html 