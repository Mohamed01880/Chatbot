"""Mise en page blanche, schémas éditables et illustrations du diaporama."""
# Cette ligne importe les dépendances nécessaires : from pathlib import Path.
from pathlib import Path
# Cette ligne importe les dépendances nécessaires : from pptx import Presentation.
from pptx import Presentation
# Cette ligne importe les dépendances nécessaires : from pptx.util import Inches, Pt.
from pptx.util import Inches, Pt
# Cette ligne importe les dépendances nécessaires : from pptx.dml.color import RGBColor.
from pptx.dml.color import RGBColor
# Cette ligne importe les dépendances nécessaires : from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR.
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
# Cette ligne importe les dépendances nécessaires : from pptx.enum.text import PP_ALIGN, MSO_ANCHOR.
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
# Cette ligne importe les dépendances nécessaires : from pptx.oxml.xmlchemy import OxmlElement.
from pptx.oxml.xmlchemy import OxmlElement

# Cette ligne exécute `W, H = 13.333, 7.5` dans le traitement courant.
W, H = 13.333, 7.5
# Cette ligne exécute `NAVY, TEAL, BLUE = '163449', '008E83', '3674C8'` dans le traitement courant.
NAVY, TEAL, BLUE = '163449', '008E83', '3674C8'
# Cette ligne exécute `INK, GRAY, LIGHT, LINE = '243E50', '617786', 'F3F7F9', 'DCE7EC'` dans le traitement courant.
INK, GRAY, LIGHT, LINE = '243E50', '617786', 'F3F7F9', 'DCE7EC'
# Cette ligne exécute `MINT, PALEBLUE, AMBER = 'E7F5F0', 'EDF3FD', 'E9A642'` dans le traitement courant.
MINT, PALEBLUE, AMBER = 'E7F5F0', 'EDF3FD', 'E9A642'
# Cette ligne affecte la variable `WHITE` avec `'FFFFFF'`.
WHITE = 'FFFFFF'

# Cette ligne définit rgb(v): return RGBColor.from_string(v), fonction qui regroupe le traitement décrit par son nom.
def rgb(v): return RGBColor.from_string(v)

# Cette ligne définit shape(s, x, y, w, h, fill=LIGHT, kind=MSO_SHAPE.ROUNDED_RECTANGLE, border=None), fonction qui regroupe le traitement décrit par son nom.
def shape(s, x, y, w, h, fill=LIGHT, kind=MSO_SHAPE.ROUNDED_RECTANGLE, border=None):
    # Cette ligne affecte la variable `q` avec `s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))`.
    q = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    # Cette ligne exécute `q.fill.solid(); q.fill.fore_color.rgb = rgb(fill)` dans le traitement courant.
    q.fill.solid(); q.fill.fore_color.rgb = rgb(fill)
    # Cette ligne vérifie la condition `border` avant d’exécuter le bloc.
    if border:
        # Cette ligne affecte la variable `q.line.color.rgb` avec `rgb(border); q.line.width = Pt(1)`.
        q.line.color.rgb = rgb(border); q.line.width = Pt(1)
    # Cette ligne démarre le cas exécuté lorsque les conditions précédentes ne sont pas satisfaites.
    else: q.line.fill.background()
    # Cette ligne vérifie la condition `kind == MSO_SHAPE.ROUNDED_RECTANGLE` avant d’exécuter le bloc.
    if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        # Cette ligne exécute `q.adjustments[0] = .12` dans le traitement courant.
        q.adjustments[0] = .12
    # Cette ligne renvoie `q` au code qui a appelé la fonction.
    return q

# Cette ligne définit txt(s, x, y, w, h, value, size=20, color=INK, bold=False, align=PP_ALIGN.LEFT), fonction qui regroupe le traitement décrit par son nom.
def txt(s, x, y, w, h, value, size=20, color=INK, bold=False, align=PP_ALIGN.LEFT):
    # Cette ligne affecte la variable `q` avec `s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))`.
    q = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    # Cette ligne affecte la variable `tf` avec `q.text_frame; tf.word_wrap = True`.
    tf = q.text_frame; tf.word_wrap = True
    # Cette ligne affecte la variable `tf.margin_left` avec `tf.margin_right = 0`.
    tf.margin_left = tf.margin_right = 0
    # Cette ligne affecte la variable `tf.margin_top` avec `tf.margin_bottom = 0`.
    tf.margin_top = tf.margin_bottom = 0
    # Cette ligne parcourt `i, line in enumerate(value.split('\n'))` pour traiter chaque élément.
    for i, line in enumerate(value.split('\n')):
        # Cette ligne affecte la variable `p` avec `tf.paragraphs[0] if i == 0 else tf.add_paragraph()`.
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        # Cette ligne affecte le texte en cours de traitement avec `line; p.font.name = 'Arial'; p.font.size = Pt(size)`.
        p.text = line; p.font.name = 'Arial'; p.font.size = Pt(size)
        # Cette ligne affecte la variable `p.font.color.rgb` avec `rgb(color); p.font.bold = bold; p.alignment = align`.
        p.font.color.rgb = rgb(color); p.font.bold = bold; p.alignment = align
        # Cette ligne affecte la variable `p.space_after` avec `Pt(7); p.line_spacing = 1.12`.
        p.space_after = Pt(7); p.line_spacing = 1.12
    # Cette ligne renvoie `q` au code qui a appelé la fonction.
    return q

# Cette ligne définit link(s, x1, y1, x2, y2, color=TEAL, arrow=True, width=2), fonction qui regroupe le traitement décrit par son nom.
def link(s, x1, y1, x2, y2, color=TEAL, arrow=True, width=2):
    # Cette ligne affecte la variable `q` avec `s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))`.
    q = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    # Cette ligne affecte la variable `q.line.color.rgb` avec `rgb(color); q.line.width = Pt(width)`.
    q.line.color.rgb = rgb(color); q.line.width = Pt(width)
    # Cette ligne vérifie la condition `arrow` avant d’exécuter le bloc.
    if arrow:
        # Cette ligne affecte la variable `end` avec `OxmlElement('a:tailEnd'); end.set('type', 'triangle'); q.line._get_or_add_ln().append(end)`.
        end = OxmlElement('a:tailEnd'); end.set('type', 'triangle'); q.line._get_or_add_ln().append(end)
    # Cette ligne renvoie `q` au code qui a appelé la fonction.
    return q

# Cette ligne définit pill(s, x, y, w, value, fill=MINT, color=TEAL, size=12), fonction qui regroupe le traitement décrit par son nom.
def pill(s, x, y, w, value, fill=MINT, color=TEAL, size=12):
    # Cette ligne exécute `shape(s, x, y, w, .38, fill)` dans le traitement courant.
    shape(s, x, y, w, .38, fill)
    # Cette ligne exécute `txt(s, x+.10, y+.075, w-.2, .25, value, size, color, True, PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s, x+.10, y+.075, w-.2, .25, value, size, color, True, PP_ALIGN.CENTER)

# Cette ligne définit badge(s, x, y, value, color=TEAL, diameter=.52), fonction qui regroupe le traitement décrit par son nom.
def badge(s, x, y, value, color=TEAL, diameter=.52):
    # Cette ligne exécute `shape(s, x, y, diameter, diameter, color, MSO_SHAPE.OVAL)` dans le traitement courant.
    shape(s, x, y, diameter, diameter, color, MSO_SHAPE.OVAL)
    # Cette ligne exécute `txt(s, x, y+.10, diameter, .3, value, 15, WHITE, True, PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s, x, y+.10, diameter, .3, value, 15, WHITE, True, PP_ALIGN.CENTER)

# Cette ligne définit icon(s, x, y, kind, color=TEAL, scale=1), fonction qui regroupe le traitement décrit par son nom.
def icon(s, x, y, kind, color=TEAL, scale=1):
    # Petits pictogrammes natifs : les formes restent éditables dans PowerPoint.
    # Cette ligne affecte la variable `z` avec `scale`.
    z=scale
    # Cette ligne vérifie la condition `kind=='doc'` avant d’exécuter le bloc.
    if kind=='doc':
        # Cette ligne exécute `shape(s,x,y,.48*z,.62*z,WHITE,MSO_SHAPE.ROUNDED_RECTANGLE,color)` dans le traitement courant.
        shape(s,x,y,.48*z,.62*z,WHITE,MSO_SHAPE.ROUNDED_RECTANGLE,color)
        # Cette ligne parcourt `k in range(3): link(s,x+.1*z,y+(.2+.12*k)*z,x+.37*z,y+(.2+.12*k)*z,color,False,1.4)` pour traiter chaque élément.
        for k in range(3): link(s,x+.1*z,y+(.2+.12*k)*z,x+.37*z,y+(.2+.12*k)*z,color,False,1.4)
    # Cette ligne teste la condition alternative `kind=='search'` si les conditions précédentes sont fausses.
    elif kind=='search':
        # Cette ligne exécute `shape(s,x,y,.40*z,.40*z,WHITE,MSO_SHAPE.OVAL,color)` dans le traitement courant.
        shape(s,x,y,.40*z,.40*z,WHITE,MSO_SHAPE.OVAL,color)
        # Cette ligne exécute `link(s,x+.33*z,y+.33*z,x+.58*z,y+.58*z,color,False,2.5)` dans le traitement courant.
        link(s,x+.33*z,y+.33*z,x+.58*z,y+.58*z,color,False,2.5)
    # Cette ligne teste la condition alternative `kind=='chat'` si les conditions précédentes sont fausses.
    elif kind=='chat':
        # Cette ligne exécute `shape(s,x,y,.62*z,.45*z,WHITE,MSO_SHAPE.ROUNDED_RECTANGLE,color)` dans le traitement courant.
        shape(s,x,y,.62*z,.45*z,WHITE,MSO_SHAPE.ROUNDED_RECTANGLE,color)
        # Cette ligne exécute `link(s,x+.12*z,y+.45*z,x+.12*z,y+.59*z,color,False)` dans le traitement courant.
        link(s,x+.12*z,y+.45*z,x+.12*z,y+.59*z,color,False)
        # Cette ligne parcourt `k in range(3): shape(s,x+(.12+.15*k)*z,y+.19*z,.055*z,.055*z,color,MSO_SHAPE.OVAL)` pour traiter chaque élément.
        for k in range(3): shape(s,x+(.12+.15*k)*z,y+.19*z,.055*z,.055*z,color,MSO_SHAPE.OVAL)
    # Cette ligne teste la condition alternative `kind=='nodes'` si les conditions précédentes sont fausses.
    elif kind=='nodes':
        # Cette ligne affecte la variable `points` avec `[(0,.12),(.45,0),(.5,.48),(.12,.57)]`.
        points=[(0,.12),(.45,0),(.5,.48),(.12,.57)]
        # Cette ligne parcourt `a,b in [(0,1),(1,2),(2,3),(3,0),(0,2)]` pour traiter chaque élément.
        for a,b in [(0,1),(1,2),(2,3),(3,0),(0,2)]:
            # Cette ligne exécute `link(s,x+(points[a][0]+.06)*z,y+(points[a][1]+.06)*z,x+(points[b][0]+.06)*z,y+(points[b][1]+.06)*z,color,False,1.4)` dans le traitement courant.
            link(s,x+(points[a][0]+.06)*z,y+(points[a][1]+.06)*z,x+(points[b][0]+.06)*z,y+(points[b][1]+.06)*z,color,False,1.4)
        # Cette ligne parcourt `a,b in points: shape(s,x+a*z,y+b*z,.13*z,.13*z,color,MSO_SHAPE.OVAL)` pour traiter chaque élément.
        for a,b in points: shape(s,x+a*z,y+b*z,.13*z,.13*z,color,MSO_SHAPE.OVAL)

# Cette ligne définit card(s,x,y,w,h,title,body,color=TEAL,fill=LIGHT,kind=None), fonction qui regroupe le traitement décrit par son nom.
def card(s,x,y,w,h,title,body,color=TEAL,fill=LIGHT,kind=None):
    # Cette ligne exécute `shape(s,x,y,w,h,fill)` dans le traitement courant.
    shape(s,x,y,w,h,fill)
    # Cette ligne vérifie la condition `kind` avant d’exécuter le bloc.
    if kind:
        # Cette ligne exécute `icon(s,x+.24,y+.24,kind,color,.8)` dans le traitement courant.
        icon(s,x+.24,y+.24,kind,color,.8)
        # Cette ligne affecte la variable `ty` avec `y+.95`.
        ty=y+.95
    # Cette ligne démarre le cas exécuté lorsque les conditions précédentes ne sont pas satisfaites.
    else: ty=y+.22
    # Cette ligne exécute `txt(s,x+.24,ty,w-.48,.65,title,20,color,True)` dans le traitement courant.
    txt(s,x+.24,ty,w-.48,.65,title,20,color,True)
    # Cette ligne exécute `txt(s,x+.24,ty+.72,w-.48,h-(ty-y)-.82,body,17,INK)` dans le traitement courant.
    txt(s,x+.24,ty+.72,w-.48,h-(ty-y)-.82,body,17,INK)

# Cette ligne définit base(prs,n,section,title,sub,footer='Prototype pédagogique • Novembre 2026'), fonction qui regroupe le traitement décrit par son nom.
def base(prs,n,section,title,sub,footer='Prototype pédagogique • Novembre 2026'):
    # Cette ligne affecte la variable `s` avec `prs.slides.add_slide(prs.slide_layouts[6])`.
    s=prs.slides.add_slide(prs.slide_layouts[6])
    # Cette ligne exécute `s.background.fill.solid(); s.background.fill.fore_color.rgb=rgb(WHITE)` dans le traitement courant.
    s.background.fill.solid(); s.background.fill.fore_color.rgb=rgb(WHITE)
    # Cette ligne exécute `shape(s,.6,.42,.12,.25,TEAL,MSO_SHAPE.RECTANGLE)` dans le traitement courant.
    shape(s,.6,.42,.12,.25,TEAL,MSO_SHAPE.RECTANGLE)
    # Cette ligne exécute `txt(s,.86,.43,10,.27,section.upper(),11,TEAL,True)` dans le traitement courant.
    txt(s,.86,.43,10,.27,section.upper(),11,TEAL,True)
    # Cette ligne exécute `txt(s,.65,1.02,12,.95,title,29,NAVY,True)` dans le traitement courant.
    txt(s,.65,1.02,12,.95,title,29,NAVY,True)
    # Cette ligne exécute `txt(s,.68,2.05,11.9,.7,sub,18,GRAY)` dans le traitement courant.
    txt(s,.68,2.05,11.9,.7,sub,18,GRAY)
    # Cette ligne exécute `link(s,.68,6.98,12.64,6.98,LINE,False,.8)` dans le traitement courant.
    link(s,.68,6.98,12.64,6.98,LINE,False,.8)
    # Cette ligne exécute `txt(s,.68,7.13,11.6,.2,footer,9,GRAY)` dans le traitement courant.
    txt(s,.68,7.13,11.6,.2,footer,9,GRAY)
    # Cette ligne exécute `txt(s,12.05,7.10,.55,.25,f'{n:02}',11,TEAL,True,PP_ALIGN.RIGHT)` dans le traitement courant.
    txt(s,12.05,7.10,.55,.25,f'{n:02}',11,TEAL,True,PP_ALIGN.RIGHT)
    # Cette ligne renvoie `s` au code qui a appelé la fonction.
    return s

# Cette ligne définit node(s,x,y,w,h,title,body='',fill=MINT,color=TEAL), fonction qui regroupe le traitement décrit par son nom.
def node(s,x,y,w,h,title,body='',fill=MINT,color=TEAL):
    # Cette ligne exécute `shape(s,x,y,w,h,fill)` dans le traitement courant.
    shape(s,x,y,w,h,fill)
    # Cette ligne exécute `txt(s,x+.15,y+.18,w-.3,.43,title,18,color,True,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,x+.15,y+.18,w-.3,.43,title,18,color,True,PP_ALIGN.CENTER)
    # Cette ligne vérifie la condition `body: txt(s,x+.15,y+.72,w-.3,h-.78,body,14,INK,False,PP_ALIGN.CENTER)` avant d’exécuter le bloc.
    if body: txt(s,x+.15,y+.72,w-.3,h-.78,body,14,INK,False,PP_ALIGN.CENTER)

# Cette ligne définit build_visual(slides, out), fonction qui regroupe le traitement décrit par son nom.
def build_visual(slides, out):
    # Cette ligne affecte la variable `out` avec `Path(out); assets=out/'assets'`.
    out=Path(out); assets=out/'assets'
    # Cette ligne affecte la variable `prs` avec `Presentation(); prs.slide_width=Inches(W); prs.slide_height=Inches(H)`.
    prs=Presentation(); prs.slide_width=Inches(W); prs.slide_height=Inches(H)

    # 01 — Une couverture éditoriale : message à gauche, univers du projet à droite.
    # Cette ligne affecte la variable `s` avec `base(prs,1,'Soutenance • Assistant d’intégration','','', 'Illustration générée par IA • Projet de chatbot d’in`.
    s=base(prs,1,'Soutenance • Assistant d’intégration','','', 'Illustration générée par IA • Projet de chatbot d’intégration')
    # Cette ligne exécute `s.shapes.add_picture(str(assets/'illustration_accueil.png'),Inches(6.65),Inches(1.45),width=Inches(6.0))` dans le traitement courant.
    s.shapes.add_picture(str(assets/'illustration_accueil.png'),Inches(6.65),Inches(1.45),width=Inches(6.0))
    # Cette ligne exécute `pill(s,.68,1.35,2.4,'INTELLIGENCE ARTIFICIELLE',size=10)` dans le traitement courant.
    pill(s,.68,1.35,2.4,'INTELLIGENCE ARTIFICIELLE',size=10)
    # Cette ligne exécute `txt(s,.68,2.0,6.0,2.25,'Mieux accueillir.\nMieux comprendre.',37,NAVY,True)` dans le traitement courant.
    txt(s,.68,2.0,6.0,2.25,'Mieux accueillir.\nMieux comprendre.',37,NAVY,True)
    # Cette ligne exécute `txt(s,.7,4.10,5.6,1.0,'Un chatbot qui retrouve l’information\navant de l’expliquer simplement.',23,GRAY)` dans le traitement courant.
    txt(s,.7,4.10,5.6,1.0,'Un chatbot qui retrouve l’information\navant de l’expliquer simplement.',23,GRAY)
    # Cette ligne exécute `pill(s,.7,5.62,1.9,'RAG HYBRIDE')` dans le traitement courant.
    pill(s,.7,5.62,1.9,'RAG HYBRIDE')
    # Cette ligne exécute `pill(s,2.8,5.62,2.2,'SOURCES VISIBLES',PALEBLUE,BLUE)` dans le traitement courant.
    pill(s,2.8,5.62,2.2,'SOURCES VISIBLES',PALEBLUE,BLUE)
    # Cette ligne exécute `txt(s,.7,6.35,10,.35,'Industrie des faisceaux de câbles  /  Présentation du prototype',15,INK)` dans le traitement courant.
    txt(s,.7,6.35,10,.35,'Industrie des faisceaux de câbles  /  Présentation du prototype',15,INK)

    # 02 — Illustration produit + trois besoins concrets, présentés en lignes.
    # Cette ligne affecte la variable `s` avec `base(prs,2,'01 / Le besoin','Les premiers jours : beaucoup de choses à comprendre','Rendre le vocabulaire, les`.
    s=base(prs,2,'01 / Le besoin','Les premiers jours : beaucoup de choses à comprendre','Rendre le vocabulaire, les zones et les explications plus accessibles.', 'Illustration générée par IA • Bénéfices attendus, non mesurés sur le terrain')
    # Cette ligne exécute `s.shapes.add_picture(str(assets/'illustration_faisceau.png'),Inches(.65),Inches(2.85),width=Inches(6.1))` dans le traitement courant.
    s.shapes.add_picture(str(assets/'illustration_faisceau.png'),Inches(.65),Inches(2.85),width=Inches(6.1))
    # Cette ligne parcourt `i,(a,b) in enumerate([('Comprendre les mots','Coupe, dénudage, sertissage…'),('Se repérer dans l’usine','À quoi sert chaque zone ?'),('Obtenir une explication','Poser sa question avec ses propres mots.')])` pour traiter chaque élément.
    for i,(a,b) in enumerate([('Comprendre les mots','Coupe, dénudage, sertissage…'),('Se repérer dans l’usine','À quoi sert chaque zone ?'),('Obtenir une explication','Poser sa question avec ses propres mots.')]):
        # Cette ligne affecte la variable `y` avec `2.92+i*1.20; badge(s,7.1,y,str(i+1)); txt(s,7.85,y,4.65,.38,a,21,NAVY,True); txt(s,7.85,y+.49,4.65,.56,b,17,GR`.
        y=2.92+i*1.20; badge(s,7.1,y,str(i+1)); txt(s,7.85,y,4.65,.38,a,21,NAVY,True); txt(s,7.85,y+.49,4.65,.56,b,17,GRAY)

    # 03 — Parcours conversationnel schématique ; aucune fausse capture.
    # Cette ligne affecte la variable `s` avec `base(prs,3,'02 / La solution','Une question naturelle. Une réponse compréhensible.','Un point d’accès simple à`.
    s=base(prs,3,'02 / La solution','Une question naturelle. Une réponse compréhensible.','Un point d’accès simple à une documentation dédiée.', 'Représentation du parcours • Ce visuel n’est pas une capture de l’application')
    # Cette ligne exécute `shape(s,.7,2.9,7.15,3.65,LIGHT)` dans le traitement courant.
    shape(s,.7,2.9,7.15,3.65,LIGHT)
    # Cette ligne exécute `shape(s,3.1,3.25,4.3,.75,PALEBLUE)` dans le traitement courant.
    shape(s,3.1,3.25,4.3,.75,PALEBLUE)
    # Cette ligne exécute `txt(s,3.3,3.47,3.9,.35,'« À quoi sert la zone P1 ? »',19,BLUE)` dans le traitement courant.
    txt(s,3.3,3.47,3.9,.35,'« À quoi sert la zone P1 ? »',19,BLUE)
    # Cette ligne exécute `shape(s,1.08,4.25,5.95,1.18,WHITE)` dans le traitement courant.
    shape(s,1.08,4.25,5.95,1.18,WHITE)
    # Cette ligne exécute `txt(s,1.32,4.43,5.47,.91,'Le chatbot cherche dans les fiches,\npuis explique avec des mots simples.',20,NAVY)` dans le traitement courant.
    txt(s,1.32,4.43,5.47,.91,'Le chatbot cherche dans les fiches,\npuis explique avec des mots simples.',20,NAVY)
    # Cette ligne exécute `pill(s,1.12,5.72,5.85,'FICHE ET SECTION CONSULTABLES',MINT,TEAL,12)` dans le traitement courant.
    pill(s,1.12,5.72,5.85,'FICHE ET SECTION CONSULTABLES',MINT,TEAL,12)
    # Cette ligne parcourt `i,(t,b) in enumerate([('Dialoguer','Question et historique'),('Expliquer','Vocabulaire accessible'),('Consulter','Sources à la demande')])` pour traiter chaque élément.
    for i,(t,b) in enumerate([('Dialoguer','Question et historique'),('Expliquer','Vocabulaire accessible'),('Consulter','Sources à la demande')]):
        # Cette ligne affecte la variable `y` avec `3.0+i*1.2; icon(s,8.5,y+.04,['chat','nodes','doc'][i],TEAL,.8); txt(s,9.25,y,3.3,.4,t,21,NAVY,True); txt(s,9.2`.
        y=3.0+i*1.2; icon(s,8.5,y+.04,['chat','nodes','doc'][i],TEAL,.8); txt(s,9.25,y,3.3,.4,t,21,NAVY,True); txt(s,9.25,y+.48,3.3,.6,b,17,GRAY)

    # 04 — Le principe, en trois grands éléments reliés.
    # Cette ligne affecte la variable `s` avec `base(prs,4,'03 / Comprendre le RAG','Le RAG : chercher d’abord, expliquer ensuite','Génération de réponse enri`.
    s=base(prs,4,'03 / Comprendre le RAG','Le RAG : chercher d’abord, expliquer ensuite','Génération de réponse enrichie par une recherche documentaire.')
    # Cette ligne affecte la variable `items` avec `[('Rechercher','Retrouver les passages\nutiles dans les fiches.','search'),('Fournir le contexte','Donner ces `.
    items=[('Rechercher','Retrouver les passages\nutiles dans les fiches.','search'),('Fournir le contexte','Donner ces passages\nau modèle de langage.','doc'),('Expliquer','Rédiger une réponse\nadaptée à la question.','chat')]
    # Cette ligne parcourt `i,(t,b,k) in enumerate(items)` pour traiter chaque élément.
    for i,(t,b,k) in enumerate(items):
        # Cette ligne affecte la variable `x` avec `.7+i*4.12; card(s,x,3.02,3.7,2.80,t,b,TEAL,MINT,k)`.
        x=.7+i*4.12; card(s,x,3.02,3.7,2.80,t,b,TEAL,MINT,k)
        # Cette ligne vérifie la condition `i<2: link(s,x+3.72,4.35,x+4.05,4.35)` avant d’exécuter le bloc.
        if i<2: link(s,x+3.72,4.35,x+4.05,4.35)
    # Cette ligne exécute `txt(s,.9,6.18,11.5,.38,'Comme un assistant qui ouvre le bon dossier avant de répondre.',22,NAVY,True,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,.9,6.18,11.5,.38,'Comme un assistant qui ouvre le bon dossier avant de répondre.',22,NAVY,True,PP_ALIGN.CENTER)

    # 05 — Le corpus : chiffres et transformation visuelle.
    # Cette ligne affecte la variable `s` avec `base(prs,5,'04 / La connaissance','Une base structurée, découpée et traçable','Chaque extrait conserve sa fich`.
    s=base(prs,5,'04 / La connaissance','Une base structurée, découpée et traçable','Chaque extrait conserve sa fiche et son titre de section.', '9 fiches et 89 extraits dans la version examinée • Contenus à valider par le site')
    # Cette ligne exécute `shape(s,.7,2.98,4.1,3.45,LIGHT)` dans le traitement courant.
    shape(s,.7,2.98,4.1,3.45,LIGHT)
    # Cette ligne exécute `txt(s,.95,3.23,1.1,1.0,'9',54,TEAL,True); txt(s,2.1,3.48,2.2,.5,'fiches',27,NAVY,True)` dans le traitement courant.
    txt(s,.95,3.23,1.1,1.0,'9',54,TEAL,True); txt(s,2.1,3.48,2.2,.5,'fiches',27,NAVY,True)
    # Cette ligne exécute `txt(s,.95,4.35,3.55,1.7,'Zones de production\nMagasins et contrôle\nSécurité et intégration\nGlossaire',19,INK)` dans le traitement courant.
    txt(s,.95,4.35,3.55,1.7,'Zones de production\nMagasins et contrôle\nSécurité et intégration\nGlossaire',19,INK)
    # Cette ligne exécute `link(s,5.02,4.37,5.85,4.37)` dans le traitement courant.
    link(s,5.02,4.37,5.85,4.37)
    # Cette ligne exécute `pill(s,4.86,3.73,1.22,'SECTIONS',LIGHT,GRAY,9)` dans le traitement courant.
    pill(s,4.86,3.73,1.22,'SECTIONS',LIGHT,GRAY,9)
    # Cette ligne exécute `shape(s,6.05,2.98,6.55,3.45,MINT)` dans le traitement courant.
    shape(s,6.05,2.98,6.55,3.45,MINT)
    # Cette ligne exécute `txt(s,6.35,3.23,1.8,1.0,'89',54,TEAL,True); txt(s,8.2,3.48,3.5,.5,'extraits utiles',27,NAVY,True)` dans le traitement courant.
    txt(s,6.35,3.23,1.8,1.0,'89',54,TEAL,True); txt(s,8.2,3.48,3.5,.5,'extraits utiles',27,NAVY,True)
    # Cette ligne parcourt `j in range(3)` pour traiter chaque élément.
    for j in range(3):
        # Cette ligne affecte la variable `y` avec `4.4+j*.48; shape(s,6.38,y,.2,.2,TEAL,MSO_SHAPE.RECTANGLE); txt(s,6.83,y-.03,5.0,.34,['Fiche : Zone de coupe P1`.
        y=4.4+j*.48; shape(s,6.38,y,.2,.2,TEAL,MSO_SHAPE.RECTANGLE); txt(s,6.83,y-.03,5.0,.34,['Fiche : Zone de coupe P1','Section : À quoi sert cette zone','Texte + provenance conservés'][j],18,INK)

    # 06 — Préparation et interrogation séparées pour éviter une chaîne trop dense.
    # Cette ligne affecte la variable `s` avec `base(prs,6,'05 / Le cœur technique','La chaîne RAG : préparer, rechercher, répondre','Le modèle de réponse reç`.
    s=base(prs,6,'05 / Le cœur technique','La chaîne RAG : préparer, rechercher, répondre','Le modèle de réponse reçoit jusqu’à 6 extraits sélectionnés.')
    # Cette ligne exécute `pill(s,.72,2.85,2.4,'AU DÉMARRAGE',LIGHT,GRAY)` dans le traitement courant.
    pill(s,.72,2.85,2.4,'AU DÉMARRAGE',LIGHT,GRAY)
    # Cette ligne parcourt `x,t,b in [(3.5,'Fiches','Découpage par section'),(6.5,'Index BM25','Index de mots-clés'),(9.5,'Embeddings','Vecteurs en mémoire')]` pour traiter chaque élément.
    for x,t,b in [(3.5,'Fiches','Découpage par section'),(6.5,'Index BM25','Index de mots-clés'),(9.5,'Embeddings','Vecteurs en mémoire')]:
        # Cette ligne exécute `node(s,x,2.82,2.5,1.15,t,b,LIGHT,NAVY)` dans le traitement courant.
        node(s,x,2.82,2.5,1.15,t,b,LIGHT,NAVY)
    # Cette ligne exécute `link(s,6.0,3.4,6.45,3.4)` dans le traitement courant.
    link(s,6.0,3.4,6.45,3.4)
    # Cette ligne exécute `link(s,4.75,3.98,4.75,4.14,TEAL,False)` dans le traitement courant.
    link(s,4.75,3.98,4.75,4.14,TEAL,False)
    # Cette ligne exécute `link(s,4.75,4.14,10.75,4.14,TEAL,False)` dans le traitement courant.
    link(s,4.75,4.14,10.75,4.14,TEAL,False)
    # Cette ligne exécute `link(s,10.75,4.14,10.75,3.99)` dans le traitement courant.
    link(s,10.75,4.14,10.75,3.99)
    # Cette ligne exécute `txt(s,.74,4.28,3.2,.3,'À CHAQUE QUESTION',12,TEAL,True)` dans le traitement courant.
    txt(s,.74,4.28,3.2,.3,'À CHAQUE QUESTION',12,TEAL,True)
    # Cette ligne affecte la variable `stages` avec `[('Question','Reformulation\nsi nécessaire'),('Recherche','Mots + sens'),('Fusion RRF','Une liste commune'),('`.
    stages=[('Question','Reformulation\nsi nécessaire'),('Recherche','Mots + sens'),('Fusion RRF','Une liste commune'),('Reranker','Reclassement'),('Réponse','Modèle + sources')]
    # Cette ligne parcourt `i,(t,b) in enumerate(stages)` pour traiter chaque élément.
    for i,(t,b) in enumerate(stages):
        # Cette ligne affecte la variable `x` avec `.72+i*2.46; node(s,x,4.9,2.18,1.55,t,b,MINT if i in (1,2,3) else PALEBLUE,TEAL if i in (1,2,3) else BLUE)`.
        x=.72+i*2.46; node(s,x,4.9,2.18,1.55,t,b,MINT if i in (1,2,3) else PALEBLUE,TEAL if i in (1,2,3) else BLUE)
        # Cette ligne vérifie la condition `i<4: link(s,x+2.19,5.65,x+2.42,5.65)` avant d’exécuter le bloc.
        if i<4: link(s,x+2.19,5.65,x+2.42,5.65)
    # Cette ligne exécute `txt(s,7.96,4.35,4.3,.32,'Jusqu’à 20 candidats → jusqu’à 6 extraits',13,GRAY)` dans le traitement courant.
    txt(s,7.96,4.35,4.3,.32,'Jusqu’à 20 candidats → jusqu’à 6 extraits',13,GRAY)

    # 07 — Deux branches réellement visibles, puis convergence.
    # Cette ligne affecte la variable `s` avec `base(prs,7,'06 / La recherche hybride','Les mots et le sens se complètent','La fusion RRF combine les position`.
    s=base(prs,7,'06 / La recherche hybride','Les mots et le sens se complètent','La fusion RRF combine les positions dans les deux classements.', 'Schéma de principe • Aucun gain de pertinence n’est déduit de ce dessin')
    # Cette ligne exécute `node(s,.75,4.0,2.35,1.25,'Question','« Préparer les fils »',PALEBLUE,BLUE)` dans le traitement courant.
    node(s,.75,4.0,2.35,1.25,'Question','« Préparer les fils »',PALEBLUE,BLUE)
    # Cette ligne exécute `node(s,4.0,2.95,3.45,1.43,'BM25','Repérer les mots précis',LIGHT,NAVY)` dans le traitement courant.
    node(s,4.0,2.95,3.45,1.43,'BM25','Repérer les mots précis',LIGHT,NAVY)
    # Cette ligne exécute `node(s,4.0,5.0,3.45,1.43,'Embeddings','Rapprocher les formulations',MINT,TEAL)` dans le traitement courant.
    node(s,4.0,5.0,3.45,1.43,'Embeddings','Rapprocher les formulations',MINT,TEAL)
    # Cette ligne exécute `node(s,9.1,4.0,3.45,1.55,'Fusion RRF','Un classement commun',PALEBLUE,BLUE)` dans le traitement courant.
    node(s,9.1,4.0,3.45,1.55,'Fusion RRF','Un classement commun',PALEBLUE,BLUE)
    # Cette ligne exécute `link(s,3.1,4.60,3.55,4.60); link(s,3.55,4.60,3.55,3.65,TEAL,False); link(s,3.55,4.60,3.55,5.70,TEAL,False)` dans le traitement courant.
    link(s,3.1,4.60,3.55,4.60); link(s,3.55,4.60,3.55,3.65,TEAL,False); link(s,3.55,4.60,3.55,5.70,TEAL,False)
    # Cette ligne exécute `link(s,3.55,3.65,3.97,3.65); link(s,3.55,5.70,3.97,5.70)` dans le traitement courant.
    link(s,3.55,3.65,3.97,3.65); link(s,3.55,5.70,3.97,5.70)
    # Cette ligne exécute `link(s,7.48,3.65,8.15,3.65,TEAL,False); link(s,7.48,5.70,8.15,5.70,TEAL,False)` dans le traitement courant.
    link(s,7.48,3.65,8.15,3.65,TEAL,False); link(s,7.48,5.70,8.15,5.70,TEAL,False)
    # Cette ligne exécute `link(s,8.15,3.65,8.15,5.70,TEAL,False); link(s,8.15,4.70,9.05,4.70)` dans le traitement courant.
    link(s,8.15,3.65,8.15,5.70,TEAL,False); link(s,8.15,4.70,9.05,4.70)

    # 08 — Le reranker visualisé comme lecture et remise en ordre.
    # Cette ligne affecte la variable `s` avec `base(prs,8,'07 / Le reranker','Relire les extraits avant de choisir','Gemini reclasse les candidats selon leur`.
    s=base(prs,8,'07 / Le reranker','Relire les extraits avant de choisir','Gemini reclasse les candidats selon leur pertinence pour la question.', 'Réglages par défaut • Étape optionnelle • Appel supplémentaire : latence et quota')
    # Cette ligne exécute `txt(s,.8,2.95,3.3,.4,'Jusqu’à 20 candidats',21,NAVY,True)` dans le traitement courant.
    txt(s,.8,2.95,3.3,.4,'Jusqu’à 20 candidats',21,NAVY,True)
    # Cette ligne parcourt `i in range(20)` pour traiter chaque élément.
    for i in range(20):
        # Cette ligne affecte la variable `x` avec `.87+(i%5)*.5; y=3.65+(i//5)*.48; shape(s,x,y,.34,.30,LINE,MSO_SHAPE.ROUNDED_RECTANGLE)`.
        x=.87+(i%5)*.5; y=3.65+(i//5)*.48; shape(s,x,y,.34,.30,LINE,MSO_SHAPE.ROUNDED_RECTANGLE)
    # Cette ligne exécute `link(s,3.65,4.5,4.42,4.5)` dans le traitement courant.
    link(s,3.65,4.5,4.42,4.5)
    # Cette ligne exécute `node(s,4.6,3.45,3.45,2.15,'Reclassement Gemini','Lecture de la question\net de chaque extrait',MINT,TEAL)` dans le traitement courant.
    node(s,4.6,3.45,3.45,2.15,'Reclassement Gemini','Lecture de la question\net de chaque extrait',MINT,TEAL)
    # Cette ligne exécute `link(s,8.2,4.5,8.94,4.5)` dans le traitement courant.
    link(s,8.2,4.5,8.94,4.5)
    # Cette ligne exécute `txt(s,9.12,2.95,3.5,.4,'Jusqu’à 6 retenus',21,NAVY,True)` dans le traitement courant.
    txt(s,9.12,2.95,3.5,.4,'Jusqu’à 6 retenus',21,NAVY,True)
    # Cette ligne parcourt `i in range(6)` pour traiter chaque élément.
    for i in range(6):
        # Cette ligne exécute `shape(s,9.2,3.57+i*.41,2.85,.29,TEAL if i==0 else MINT)` dans le traitement courant.
        shape(s,9.2,3.57+i*.41,2.85,.29,TEAL if i==0 else MINT)
        # Cette ligne exécute `txt(s,9.32,3.61+i*.41,2.5,.2,f'{i+1}   Extrait sélectionné',11,WHITE if i==0 else TEAL)` dans le traitement courant.
        txt(s,9.32,3.61+i*.41,2.5,.2,f'{i+1}   Extrait sélectionné',11,WHITE if i==0 else TEAL)
    # Cette ligne exécute `pill(s,2.1,6.28,9.1,'SORTIE INVALIDE ? LE CLASSEMENT INITIAL EST CONSERVÉ.',LIGHT,GRAY,12)` dans le traitement courant.
    pill(s,2.1,6.28,9.1,'SORTIE INVALIDE ? LE CLASSEMENT INITIAL EST CONSERVÉ.',LIGHT,GRAY,12)

    # 09 — Question, source et exemple de réponse : aucune capture inventée.
    # Cette ligne affecte la variable `s` avec `base(prs,9,'08 / Un exemple concret','Retrouver P1 sans que l’utilisateur dise « P1 »','« Où prépare-t-on les `.
    s=base(prs,9,'08 / Un exemple concret','Retrouver P1 sans que l’utilisateur dise « P1 »','« Où prépare-t-on les fils à la bonne longueur avant de les assembler ? »', 'Réponse illustrée • Source : fiche Zone de coupe P1, section « À quoi sert cette zone »')
    # Cette ligne exécute `card(s,.75,3.1,5.25,2.65,'Le passage documentaire','« Ces machines coupent les fils\nà la longueur demandée. »',TEAL,MINT,'doc')` dans le traitement courant.
    card(s,.75,3.1,5.25,2.65,'Le passage documentaire','« Ces machines coupent les fils\nà la longueur demandée. »',TEAL,MINT,'doc')
    # Cette ligne exécute `link(s,6.15,4.48,6.85,4.48)` dans le traitement courant.
    link(s,6.15,4.48,6.85,4.48)
    # Cette ligne exécute `card(s,7.05,3.1,5.55,2.65,'Une explication simple','« La zone P1 coupe les fils à la bonne\nlongueur avant les étapes suivantes. »` dans le traitement courant.
    card(s,7.05,3.1,5.55,2.65,'Une explication simple','« La zone P1 coupe les fils à la bonne\nlongueur avant les étapes suivantes. »',BLUE,PALEBLUE,'chat')
    # Cette ligne exécute `txt(s,1.1,6.2,11.0,.43,'La bonne information doit être retrouvée avant d’être reformulée.',21,NAVY,True,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,1.1,6.2,11.0,.43,'La bonne information doit être retrouvée avant d’être reformulée.',21,NAVY,True,PP_ALIGN.CENTER)

    # 10 — Architecture avec liens réels vers les deux types de données.
    # Cette ligne affecte la variable `s` avec `base(prs,10,'09 / L’architecture','Des composants aux rôles bien séparés','Le modèle d’embeddings et le modèle`.
    s=base(prs,10,'09 / L’architecture','Des composants aux rôles bien séparés','Le modèle d’embeddings et le modèle de réponse sont indépendants.', 'PostgreSQL stocke comptes et échanges • Les vecteurs sont en mémoire, pas dans PostgreSQL')
    # Cette ligne exécute `node(s,.75,3.8,2.42,1.65,'Interface web','HTML / CSS / JS',PALEBLUE,BLUE)` dans le traitement courant.
    node(s,.75,3.8,2.42,1.65,'Interface web','HTML / CSS / JS',PALEBLUE,BLUE)
    # Cette ligne exécute `node(s,3.88,3.8,2.42,1.65,'API FastAPI','Orchestration',LIGHT,NAVY)` dans le traitement courant.
    node(s,3.88,3.8,2.42,1.65,'API FastAPI','Orchestration',LIGHT,NAVY)
    # Cette ligne exécute `node(s,7.01,3.8,2.42,1.65,'Moteur RAG','BM25 + vecteurs\nFusion + reranker',MINT,TEAL)` dans le traitement courant.
    node(s,7.01,3.8,2.42,1.65,'Moteur RAG','BM25 + vecteurs\nFusion + reranker',MINT,TEAL)
    # Cette ligne exécute `node(s,10.14,3.8,2.42,1.65,'Modèle','Gemini / Ollama\nou Claude',PALEBLUE,BLUE)` dans le traitement courant.
    node(s,10.14,3.8,2.42,1.65,'Modèle','Gemini / Ollama\nou Claude',PALEBLUE,BLUE)
    # Cette ligne parcourt `x in (3.2,6.33,9.46): link(s,x,4.62,x+.62,4.62)` pour traiter chaque élément.
    for x in (3.2,6.33,9.46): link(s,x,4.62,x+.62,4.62)
    # Cette ligne exécute `node(s,3.88,5.96,2.42,.7,'PostgreSQL','',LIGHT,NAVY)` dans le traitement courant.
    node(s,3.88,5.96,2.42,.7,'PostgreSQL','',LIGHT,NAVY)
    # Cette ligne exécute `link(s,5.1,5.49,5.1,5.91,GRAY)` dans le traitement courant.
    link(s,5.1,5.49,5.1,5.91,GRAY)
    # Cette ligne exécute `pill(s,6.93,2.86,2.6,'FICHES + OLLAMA',MINT,TEAL,11)` dans le traitement courant.
    pill(s,6.93,2.86,2.6,'FICHES + OLLAMA',MINT,TEAL,11)
    # Cette ligne exécute `link(s,8.22,3.30,8.22,3.75)` dans le traitement courant.
    link(s,8.22,3.30,8.22,3.75)
    # Cette ligne exécute `txt(s,9.95,6.02,2.75,.6,'Cloud ou local,\nselon configuration',14,GRAY,False,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,9.95,6.02,2.75,.6,'Cloud ou local,\nselon configuration',14,GRAY,False,PP_ALIGN.CENTER)

    # 11 — Résilience : déclencheur vers comportement de repli.
    # Cette ligne affecte la variable `s` avec `base(prs,11,'10 / La robustesse','Prévoir les erreurs pour garder un service utile','Le point de contrôle /hea`.
    s=base(prs,11,'10 / La robustesse','Prévoir les erreurs pour garder un service utile','Le point de contrôle /health permet de consulter l’état technique.')
    # Cette ligne affecte la variable `rows` avec `[('Embeddings indisponibles','Recherche BM25 conservée'),('Reranker en échec','Classement initial conservé'),(`.
    rows=[('Embeddings indisponibles','Recherche BM25 conservée'),('Reranker en échec','Classement initial conservé'),('Information absente','Consigne de reconnaître le manque')]
    # Cette ligne parcourt `i,(a,b) in enumerate(rows)` pour traiter chaque élément.
    for i,(a,b) in enumerate(rows):
        # Cette ligne affecte la variable `y` avec `3.0+i*1.05; shape(s,.8,y,4.8,.78,LIGHT); txt(s,1.03,y+.23,4.35,.34,a,19,INK)`.
        y=3.0+i*1.05; shape(s,.8,y,4.8,.78,LIGHT); txt(s,1.03,y+.23,4.35,.34,a,19,INK)
        # Cette ligne exécute `link(s,5.82,y+.39,6.45,y+.39)` dans le traitement courant.
        link(s,5.82,y+.39,6.45,y+.39)
        # Cette ligne exécute `shape(s,6.7,y,5.8,.78,MINT); txt(s,6.93,y+.23,5.33,.34,b,19,TEAL,True)` dans le traitement courant.
        shape(s,6.7,y,5.8,.78,MINT); txt(s,6.93,y+.23,5.33,.34,b,19,TEAL,True)
    # Cette ligne exécute `txt(s,1.0,6.39,11.3,.3,'Disponibilité technique et exactitude des réponses sont deux sujets à évaluer.',16,GRAY,False,PP_ALIGN.CEN` dans le traitement courant.
    txt(s,1.0,6.39,11.3,.3,'Disponibilité technique et exactitude des réponses sont deux sujets à évaluer.',16,GRAY,False,PP_ALIGN.CENTER)

    # 12 — Les mêmes données, en barres proportionnelles et dénominateur visible.
    # Cette ligne affecte la variable `s` avec `base(prs,12,'11 / Les résultats','BM25 : la section attendue dans les premiers résultats','32 questions • Rech`.
    s=base(prs,12,'11 / Les résultats','BM25 : la section attendue dans les premiers résultats','32 questions • Recherche documentaire seule • Mesure du 15 novembre 2026', 'Ne mesure pas la justesse des réponses finales • Gain hybride/reranker encore à évaluer')
    # Cette ligne parcourt `i,(name,v,num) in enumerate([('Hit@1',.5,'16 / 32'),('Hit@3',.875,'28 / 32'),('Hit@6',1.0,'32 / 32')])` pour traiter chaque élément.
    for i,(name,v,num) in enumerate([('Hit@1',.5,'16 / 32'),('Hit@3',.875,'28 / 32'),('Hit@6',1.0,'32 / 32')]):
        # Cette ligne affecte la variable `y` avec `3.05+i*1.05; txt(s,.8,y+.12,1.25,.4,name,21,NAVY,True)`.
        y=3.05+i*1.05; txt(s,.8,y+.12,1.25,.4,name,21,NAVY,True)
        # Cette ligne exécute `shape(s,2.25,y,5.55,.65,LIGHT)` dans le traitement courant.
        shape(s,2.25,y,5.55,.65,LIGHT)
        # Cette ligne exécute `shape(s,2.25,y,5.55*v,.65,TEAL if i==2 else BLUE)` dans le traitement courant.
        shape(s,2.25,y,5.55*v,.65,TEAL if i==2 else BLUE)
        # Cette ligne exécute `txt(s,8.0,y+.1,1.55,.43,num,21,NAVY,True)` dans le traitement courant.
        txt(s,8.0,y+.1,1.55,.43,num,21,NAVY,True)
    # Cette ligne exécute `txt(s,2.25,6.23,7.1,.45,'50 %  →  87,5 %  →  100 % dans le jeu actuel',19,GRAY)` dans le traitement courant.
    txt(s,2.25,6.23,7.1,.45,'50 %  →  87,5 %  →  100 % dans le jeu actuel',19,GRAY)
    # Cette ligne exécute `shape(s,10.03,2.98,2.48,3.49,MINT)` dans le traitement courant.
    shape(s,10.03,2.98,2.48,3.49,MINT)
    # Cette ligne exécute `txt(s,10.23,3.25,2.08,.82,'12',42,TEAL,True,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,10.23,3.25,2.08,.82,'12',42,TEAL,True,PP_ALIGN.CENTER)
    # Cette ligne exécute `txt(s,10.23,4.12,2.08,.85,'tests réussis',18,TEAL,True,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,10.23,4.12,2.08,.85,'tests réussis',18,TEAL,True,PP_ALIGN.CENTER)
    # Cette ligne exécute `txt(s,10.23,4.94,2.08,.38,'Services simulés',12,GRAY,False,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,10.23,4.94,2.08,.38,'Services simulés',12,GRAY,False,PP_ALIGN.CENTER)
    # Cette ligne exécute `link(s,10.3,5.49,12.24,5.49,LINE,False,1)` dans le traitement courant.
    link(s,10.3,5.49,12.24,5.49,LINE,False,1)
    # Cette ligne exécute `txt(s,10.23,5.80,2.08,.43,'MRR : 0,69',21,NAVY,True,PP_ALIGN.CENTER)` dans le traitement courant.
    txt(s,10.23,5.80,2.08,.43,'MRR : 0,69',21,NAVY,True,PP_ALIGN.CENTER)

    # 13 — Démo chronologique, espacée et facile à suivre.
    # Cette ligne affecte la variable `s` avec `base(prs,13,'12 / La démonstration','Trois questions pour montrer le comportement','Sources visibles • Une nou`.
    s=base(prs,13,'12 / La démonstration','Trois questions pour montrer le comportement','Sources visibles • Une nouvelle conversation pour chaque essai')
    # Cette ligne exécute `link(s,1.04,3.23,1.04,6.15,LINE,False,3)` dans le traitement courant.
    link(s,1.04,3.23,1.04,6.15,LINE,False,3)
    # Cette ligne parcourt `i,(a,b,c) in enumerate([` pour traiter chaque élément.
    for i,(a,b,c) in enumerate([
        # Cette ligne exécute `('Question directe','« À quoi sert la zone de coupe P1 ? »','Observer l’explication et la source.'),` dans le traitement courant.
        ('Question directe','« À quoi sert la zone de coupe P1 ? »','Observer l’explication et la source.'),
        # Cette ligne exécute `('Même idée, autres mots','« Où prépare-t-on les fils à la bonne longueur ? »','Vérifier que P1 est retrouvée.'),` dans le traitement courant.
        ('Même idée, autres mots','« Où prépare-t-on les fils à la bonne longueur ? »','Vérifier que P1 est retrouvée.'),
        # Cette ligne démarre le bloc `('Information non documentée','« Combien de jours de congé ai-je par an ? »','Vérifier que le bot ne devine pas.')])`.
        ('Information non documentée','« Combien de jours de congé ai-je par an ? »','Vérifier que le bot ne devine pas.')]):
        # Cette ligne affecte la variable `y` avec `3.0+i*1.14; badge(s,.78,y,str(i+1)); txt(s,1.58,y,4.7,.38,a,20,NAVY,True)`.
        y=3.0+i*1.14; badge(s,.78,y,str(i+1)); txt(s,1.58,y,4.7,.38,a,20,NAVY,True)
        # Cette ligne exécute `txt(s,1.58,y+.46,8.5,.43,b,18,INK); txt(s,8.85,y,3.7,.85,c,17,TEAL)` dans le traitement courant.
        txt(s,1.58,y+.46,8.5,.43,b,18,INK); txt(s,8.85,y,3.7,.85,c,17,TEAL)

    # 14 — Réalisé et suite : distinguer visuellement les deux.
    # Cette ligne affecte la variable `s` avec `base(prs,14,'13 / Bilan et perspectives','Un prototype intégré, une progression mesurable','La prochaine étape`.
    s=base(prs,14,'13 / Bilan et perspectives','Un prototype intégré, une progression mesurable','La prochaine étape : confirmer la qualité avec les utilisateurs.')
    # Cette ligne exécute `shape(s,.75,2.98,5.52,3.55,MINT)` dans le traitement courant.
    shape(s,.75,2.98,5.52,3.55,MINT)
    # Cette ligne exécute `pill(s,1.02,3.23,1.9,'RÉALISÉ',WHITE,TEAL)` dans le traitement courant.
    pill(s,1.02,3.23,1.9,'RÉALISÉ',WHITE,TEAL)
    # Cette ligne exécute `txt(s,1.03,3.95,4.94,2.1,'Base documentaire structurée\nRecherche hybride + reranker\nDialogue et sources visibles\nTests et évalu` dans le traitement courant.
    txt(s,1.03,3.95,4.94,2.1,'Base documentaire structurée\nRecherche hybride + reranker\nDialogue et sources visibles\nTests et évaluation initiale',21,NAVY)
    # Cette ligne exécute `shape(s,6.61,2.98,5.96,3.55,LIGHT)` dans le traitement courant.
    shape(s,6.61,2.98,5.96,3.55,LIGHT)
    # Cette ligne exécute `pill(s,6.90,3.23,2.1,'À VALIDER',WHITE,BLUE)` dans le traitement courant.
    pill(s,6.90,3.23,2.1,'À VALIDER',WHITE,BLUE)
    # Cette ligne exécute `txt(s,6.91,3.95,5.35,2.1,'Comparer les 3 modes de recherche\nFaire approuver les fiches métier\nMesurer qualité, délai et coût\nRe` dans le traitement courant.
    txt(s,6.91,3.95,5.35,2.1,'Comparer les 3 modes de recherche\nFaire approuver les fiches métier\nMesurer qualité, délai et coût\nRenforcer la sécurité applicative',20,INK)

    # 15 — Conclusion mémorable ; image en rappel et message unique.
    # Cette ligne affecte la variable `s` avec `base(prs,15,'14 / Conclusion','','', 'Illustration générée par IA • Merci pour votre attention')`.
    s=base(prs,15,'14 / Conclusion','','', 'Illustration générée par IA • Merci pour votre attention')
    # Cette ligne exécute `txt(s,.72,1.4,7.0,2.15,'Rendre le savoir technique\nplus accessible.',35,NAVY,True)` dans le traitement courant.
    txt(s,.72,1.4,7.0,2.15,'Rendre le savoir technique\nplus accessible.',35,NAVY,True)
    # Cette ligne exécute `txt(s,.76,3.55,6.25,1.7,'Retrouver l’information utile.\nLa sélectionner avec soin.\nL’expliquer simplement.',25,TEAL)` dans le traitement courant.
    txt(s,.76,3.55,6.25,1.7,'Retrouver l’information utile.\nLa sélectionner avec soin.\nL’expliquer simplement.',25,TEAL)
    # Cette ligne exécute `s.shapes.add_picture(str(assets/'illustration_accueil.png'),Inches(7.18),Inches(2.10),width=Inches(5.5))` dans le traitement courant.
    s.shapes.add_picture(str(assets/'illustration_accueil.png'),Inches(7.18),Inches(2.10),width=Inches(5.5))
    # Cette ligne exécute `pill(s,.76,5.82,4.95,'UNE CHAÎNE RAG AU SERVICE DE L’INTÉGRATION',MINT,TEAL,11)` dans le traitement courant.
    pill(s,.76,5.82,4.95,'UNE CHAÎNE RAG AU SERVICE DE L’INTÉGRATION',MINT,TEAL,11)
    # Cette ligne exécute `txt(s,.76,6.39,8,.37,'Merci pour votre attention.  /  Vos questions',20,NAVY,True)` dans le traitement courant.
    txt(s,.76,6.39,8,.37,'Merci pour votre attention.  /  Vos questions',20,NAVY,True)

    # 16 — Réserve pour les réponses au jury.
    # Cette ligne affecte la variable `s` avec `base(prs,16,'Annexe / Questions du jury','Trois choix techniques à défendre','À ouvrir pendant les échanges, s`.
    s=base(prs,16,'Annexe / Questions du jury','Trois choix techniques à défendre','À ouvrir pendant les échanges, selon les questions du jury.')
    # Cette ligne parcourt `i,(title,body) in enumerate([` pour traiter chaque élément.
    for i,(title,body) in enumerate([
        # Cette ligne exécute `('Pourquoi le RAG ?','Mettre à jour les fiches sans réentraîner le modèle de réponse.'),` dans le traitement courant.
        ('Pourquoi le RAG ?','Mettre à jour les fiches sans réentraîner le modèle de réponse.'),
        # Cette ligne exécute `('Pourquoi des vecteurs en mémoire ?','89 extraits : un choix simple pour ce prototype. La persistance reste à étudier.'),` dans le traitement courant.
        ('Pourquoi des vecteurs en mémoire ?','89 extraits : un choix simple pour ce prototype. La persistance reste à étudier.'),
        # Cette ligne démarre le bloc `('Le RAG évite-t-il toute erreur ?','Non. Il faut évaluer les documents retrouvés et la réponse produite.')])`.
        ('Le RAG évite-t-il toute erreur ?','Non. Il faut évaluer les documents retrouvés et la réponse produite.')]):
        # Cette ligne affecte la variable `y` avec `3.03+i*1.14; shape(s,.78,y,11.77,.94,LIGHT)`.
        y=3.03+i*1.14; shape(s,.78,y,11.77,.94,LIGHT)
        # Cette ligne exécute `txt(s,1.04,y+.24,4.65,.5,title,19,TEAL,True)` dans le traitement courant.
        txt(s,1.04,y+.24,4.65,.5,title,19,TEAL,True)
        # Cette ligne exécute `txt(s,5.96,y+.18,6.30,.65,body,17,INK)` dans le traitement courant.
        txt(s,5.96,y+.18,6.30,.65,body,17,INK)

    # Notes orales conservées, avec précisions liées aux nouveaux visuels.
    # Cette ligne parcourt `n,(s,data) in enumerate(zip(prs.slides,slides),1)` pour traiter chaque élément.
    for n,(s,data) in enumerate(zip(prs.slides,slides),1):
        # Cette ligne exécute `speech,duration=data[3],data[4]` dans le traitement courant.
        speech,duration=data[3],data[4]
        # Cette ligne affecte la variable `extra` avec `''`.
        extra=''
        # Cette ligne vérifie la condition `n in (1,2,15): extra='\n\nVisuel : illustration générée par IA, sans représentation d’un site réel.'` avant d’exécuter le bloc.
        if n in (1,2,15): extra='\n\nVisuel : illustration générée par IA, sans représentation d’un site réel.'
        # Cette ligne vérifie la condition `n in (6,7,8,10): extra='\n\nConseil oral : suivre les flèches du schéma avec le pointeur, sans lire tous les libellés.'` avant d’exécuter le bloc.
        if n in (6,7,8,10): extra='\n\nConseil oral : suivre les flèches du schéma avec le pointeur, sans lire tous les libellés.'
        # Cette ligne vérifie la condition `n==12: extra='\n\nLes barres représentent 16, 28 et 32 questions sur 32. Les 12 tests sont une validation technique séparée, avec services externes simulés.'` avant d’exécuter le bloc.
        if n==12: extra='\n\nLes barres représentent 16, 28 et 32 questions sur 32. Les 12 tests sont une validation technique séparée, avec services externes simulés.'
        # Cette ligne affecte le texte en cours de traitement avec `f'Durée indicative : {duration} secondes.\n\n{speech}{extra}'`.
        s.notes_slide.notes_text_frame.text=f'Durée indicative : {duration} secondes.\n\n{speech}{extra}'
    # Cette ligne affecte la variable `prs.core_properties.title` avec `'Chatbot d’intégration — Soutenance RAG'`.
    prs.core_properties.title='Chatbot d’intégration — Soutenance RAG'
    # Cette ligne affecte la variable `prs.core_properties.subject` avec `'Version visuelle : fond blanc, illustrations et schémas'`.
    prs.core_properties.subject='Version visuelle : fond blanc, illustrations et schémas'
    # Cette ligne affecte la variable `prs.core_properties.author` avec `'Projet Chatbot'`.
    prs.core_properties.author='Projet Chatbot'
    # Cette ligne exécute `prs.save(out/'Presentation_Chatbot_RAG_Visuelle.pptx')` dans le traitement courant.
    prs.save(out/'Presentation_Chatbot_RAG_Visuelle.pptx')
    # Cette ligne renvoie `prs` au code qui a appelé la fonction.
    return prs
# Cette ligne exécute `"""Utilitaires de dessin réutilisés pour créer les schémas de la présentation."""` dans le traitement courant.
"""Utilitaires de dessin réutilisés pour créer les schémas de la présentation."""

