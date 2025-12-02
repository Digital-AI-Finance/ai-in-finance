"""Update team page to use downloaded photos."""
import re
from pathlib import Path

# Mapping of name patterns to photo files
PHOTO_MAP = {
    'j.vanhillegersberg': 'j_vanhillegersberg.jpg',
    'jvanhillegersberg': 'j_vanhillegersberg.jpg',
    'm.r.k.mes': 'm_r_k_mes.jpg',
    'mrkmes': 'm_r_k_mes.jpg',
    'joerg.osterrieder': 'joerg_osterrieder.jpg',
    'joergosterrieder': 'joerg_osterrieder.jpg',
    'osterrieder': 'joerg_osterrieder.jpg',
    'm.r.machado': 'm_r_machado.jpg',
    'mrmachado': 'm_r_machado.jpg',
    'x.huang': 'x_huang.jpg',
    'xhuang': 'x_huang.jpg',
    'f.s.bernard': 'f_s_bernard.jpg',
    'fsbernard': 'f_s_bernard.jpg',
    'c.kolb': 'c_kolb.jpg',
    'ckolb': 'c_kolb.jpg',
    'r.effing': 'r_effing.jpg',
    'reffing': 'r_effing.jpg',
    'a.trivella': 'a_trivella.jpg',
    'atrivella': 'a_trivella.jpg',
    'p.khrennikova': 'p_khrennikova.jpg',
    'pkhrennikova': 'p_khrennikova.jpg',
    'j.huellmann': 'j_huellmann.jpg',
    'jhuellmann': 'j_huellmann.jpg',
    'e.svetlova': 'e_svetlova.jpg',
    'esvetlova': 'e_svetlova.jpg',
    'r.guizzardi': 'r_guizzardi.jpg',
    'rguizzardi': 'r_guizzardi.jpg',
    'mathis.jander': 'mathis_jander.jpg',
    'mathisjander': 'mathis_jander.jpg',
    'mohamed.faid': 'mohamed_faid.jpg',
    'mohamedfaid': 'mohamed_faid.jpg',
    'armin.sadighi': 'armin_sadighi.jpg',
    'arminsadighi': 'armin_sadighi.jpg',
    'w.j.a.vanheeswijk': 'w_j_a_vanheeswijk.jpg',
    'wjavanheeswijk': 'w_j_a_vanheeswijk.jpg',
    'manuele.massei': 'manuele_massei.jpg',
    'manuelemassei': 'manuele_massei.jpg',
}

team_file = Path("content/our-people/our-team/_index.md")
content = team_file.read_text(encoding='utf-8')
original = content

# Pattern: ![...](images/.wh/ea/uc/.../name.avif)
pattern = r'!\[([^\]]*)\]\(images/\.wh/ea/uc/[^/]+/([^)]+)\)'

def replace_img(match):
    alt = match.group(1)
    filename = match.group(2).lower().replace('.avif', '').replace('.jpg', '').replace('.png', '')

    # Find matching photo
    for key, photo in PHOTO_MAP.items():
        if key in filename:
            return f'![{alt}](images/team/{photo})'

    # No match, keep original
    return match.group(0)

content = re.sub(pattern, replace_img, content)

if content != original:
    team_file.write_text(content, encoding='utf-8')
    count = len(re.findall(pattern, original))
    print(f"Updated {count} image references")
else:
    print("No changes made")
