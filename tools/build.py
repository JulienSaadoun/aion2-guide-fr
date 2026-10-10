#!/usr/bin/env python3
"""Génère gladiateur.html à partir de tools/sections/*.html.
Balises : [[slug]] -> icône + nom FR (EN) ; [[slug|court]] -> icône + nom FR seul.
{{texte FR*|English}} -> nom non confirmé (astérisque + anglais)."""
import os, re, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Noms français : client FR d'Aion 2 global, tels qu'affichés par metabot.gg/fr (données du jeu).
NAMES = {
 "keen-strike": ("Coup acéré", "Keen Strike"),
 "rending-blow": ("Coup féroce lacérant", "Rending Blow"),
 "overhead-slam": ("Fracas", "Overhead Slam"),
 "ruinous-blow": ("Coup féroce anéantissant", "Ruinous Blow"),
 "leaping-slam": ("Frappe bondissante", "Leaping Slam"),
 "rush-strike": ("Coup de ruée", "Rush Strike"),
 "crushing-wave": ("Onde broyeuse", "Crushing Wave"),
 "sword-aura-rampage": ("Lame déferlante", "Sword Aura Rampage"),
 "mocking-blade": ("Épée dévastatrice", "Mocking Blade"),
 "ankle-slice": ("Entaille de chevilles", "Ankle Slice"),
 "aerial-snare": ("Contrainte aérienne", "Aerial Snare"),
 "assault-strike": ("Frappe d'assaut", "Assault Strike"),
 "fracturing-rush": ("Ruée fracturante", "Fracturing Rush"),
 "defiance": ("Dissipation de choc", "Defiance"),
 "lunge-stance": ("Position de charge", "Lunge Stance"),
 "zikels-blessing": ("Bénédiction de Zikel", "Zikel's Blessing"),
 "rage-burst": ("Explosion de fureur", "Rage Burst"),
 "focused-block": ("Blocage ciblé", "Focused Block"),
 "blade-toss": ("Lancer de lame", "Blade Toss"),
 "lifestealing-blade": ("Lame vampirique", "Lifestealing Blade"),
 "wave-armor": ("Armure d'onde", "Wave Armor"),
 "armor-of-balance": ("Armure d'équilibre", "Armor of Balance"),
 "tenaciousness": ("Persévérance", "Tenaciousness"),
 "forced-restraint": ("Contrainte forcée", "Forced Restraint"),
 "wrath-wave": ("Onde de rage", "Wrath Wave"),
 "experienced-counterstrike": ("Riposte habile", "Experienced Counterstrike"),
 "attack-preparation": ("Préparation d'attaque", "Attack Preparation"),
 "murderous-burst": ("Rupture meurtrière", "Murderous Burst"),
 "impact-hit": ("Coup de choc", "Impact Hit"),
 "identify-weakness": ("Détection des faiblesses", "Identify Weakness"),
 "blood-absorption": ("Drain de sang", "Blood Absorption"),
 "survival-stance": ("Position de survie", "Survival Stance"),
 "survival-willpower": ("Volonté de survie", "Survival Willpower"),
 "protection-armor": ("Armure de protection", "Protection Armor"),
 "destructive-impulse": ("Impulsion destructrice", "Destructive Impulse"),
}

def sk(m):
    slug, short = m.group(1), m.group(2)
    fr, en = NAMES[slug]
    img = f'<img src="assets/icons/{slug}.jpg" alt="" loading="lazy">'
    if short is not None:
        return f'<span class="sk">{img}{html.escape(fr)}</span>'
    return f'<span class="sk">{img}{html.escape(fr)} <span class="en">({html.escape(en)})</span></span>'

def nc(m):
    fr, en = m.group(1), m.group(2)
    return f'{html.escape(fr)}<span class="nc">*</span> <span class="en muted">({html.escape(en)})</span>'

def big(slug, lv, text, chips=()):
    fr, en = NAMES[slug]
    c = ''.join(f'<span class="chip">{x}</span>' for x in chips)
    lvh = f'<span class="lv">{lv}</span>' if lv else ''
    return (f'<div class="skill"><img src="assets/icons/{slug}.jpg" alt="" loading="lazy"><div>'
            f'<div class="name">{html.escape(fr)} <span class="en">({html.escape(en)})</span>{lvh}</div>'
            f'<p>{text}</p>' + (f'<div class="chips">{c}</div>' if c else '') + '</div></div>')

def expand(s):
    s = re.sub(r'\{\{([^|}]+)\|([^}]+)\}\}', nc, s)
    s = re.sub(r'\[\[([a-z-]+)(?:\|(court))?\]\]', sk, s)
    s = re.sub(r'\[\[big:([a-z-]+)\|([^|\]]*)\|([^\]]*?)(?:\|\|([^\]]*))?\]\]',
               lambda m: big(m.group(1), m.group(2), m.group(3), [x for x in (m.group(4) or '').split(';;') if x]), s)
    return s

def main():
    secs = sorted(glob.glob(os.path.join(ROOT, 'tools', 'sections', '*.html')))
    toc, body = [], []
    for i, f in enumerate(secs, 1):
        raw = open(f, encoding='utf-8').read()
        title = raw.splitlines()[0].strip()
        sid = re.sub(r'^\d+-', '', os.path.basename(f)[:-5])
        content = expand('\n'.join(raw.splitlines()[1:]))
        toc.append(f'<a href="#{sid}">{i}. {html.escape(title)}</a>')
        body.append(f'<section id="{sid}"><div class="sec-head"><div class="sec-num">{i}</div><h2>{html.escape(title)}</h2></div>\n{content}\n</section>')
    tpl = open(os.path.join(ROOT, 'tools', 'page.tpl.html'), encoding='utf-8').read()
    out = tpl.replace('%%TOC%%', '\n'.join(toc)).replace('%%BODY%%', '\n'.join(body))
    open(os.path.join(ROOT, 'gladiateur.html'), 'w', encoding='utf-8').write(out)
    print('ok', len(secs), 'sections')

if __name__ == '__main__':
    main()
