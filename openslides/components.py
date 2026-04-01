"""
Slide Component System
Renders individual slide types from configuration.
"""

from typing import Dict, Any, Optional, List
from .theme import (
    Theme, DarkTheme, LightTheme, PitchDarkTheme, PitchLightTheme,
    ConsultingDarkTheme, ConsultingLightTheme,
    ConsumerDarkTheme, ConsumerLightTheme,
    CreativeDarkTheme, CreativeLightTheme,
    MinimalDarkTheme, MinimalLightTheme,
    SalesDarkTheme, SalesLightTheme,
)


def _get_base_html(theme: Theme) -> str:
    """Generate base HTML document structure."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      color: {theme.text_primary};
      margin-bottom: 60px;
    }}
  </style>
'''


def _close_html() -> str:
    """Close HTML document."""
    return '''
</body>
</html>'''


class SlideRenderer:
    """Static methods for rendering each slide type."""

    @staticmethod
    def render_title_slide(
        company_name: str,
        headline: str,
        subheadline: str,
        bottom_items: Optional[List[str]] = None,
        logo_url: Optional[str] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render title slide with style-specific layouts.
        """
        theme = theme or DarkTheme()
        bottom_items = bottom_items or []
        style = getattr(theme, 'name', 'dark')

        # CONSULTING STYLE - Centered, formal, horizontal rules
        if 'consulting' in style:
            bottom_html = " · ".join(bottom_items) if bottom_items else ""
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{company_name}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}
    .top-bar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 8px;
      background: {theme.accent};
    }}
    .company {{
      font-family: {theme.headline_font_family};
      font-size: 28px;
      font-weight: 500;
      letter-spacing: 0.3em;
      text-transform: uppercase;
      color: {theme.text_secondary};
      margin-bottom: 60px;
    }}
    .divider {{
      width: 120px;
      height: 2px;
      background: {theme.accent};
      margin: 40px auto;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 72px;
      font-weight: 600;
      line-height: 1.15;
      max-width: 1100px;
      margin-bottom: 0;
      color: {theme.text_primary};
    }}
    .subhead {{
      font-size: 22px;
      color: {theme.text_secondary};
      max-width: 700px;
      line-height: 1.6;
      margin-top: 40px;
    }}
    .bottom {{
      position: absolute;
      bottom: 80px;
      font-size: 14px;
      color: {theme.text_muted};
      letter-spacing: 0.05em;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="company">{company_name}</div>
  <h1 class="headline">{headline.replace(chr(10), "<br>")}</h1>
  <div class="divider"></div>
  <p class="subhead">{subheadline}</p>
  <div class="bottom">{bottom_html}</div>
</body>
</html>'''

        # CONSUMER STYLE - Playful, gradient accent, rounded
        elif 'consumer' in style:
            bottom_items_html = "".join(
                f'<span class="pill">{item}</span>' for item in bottom_items
            )
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{company_name}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 100px 120px;
      position: relative;
      overflow: hidden;
    }}
    .gradient-blob {{
      position: absolute;
      width: 800px;
      height: 800px;
      border-radius: 50%;
      background: {theme.gradient_primary};
      opacity: 0.15;
      filter: blur(100px);
      top: -200px;
      right: -200px;
    }}
    .gradient-blob-2 {{
      position: absolute;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      background: {theme.accent_secondary};
      opacity: 0.1;
      filter: blur(80px);
      bottom: -100px;
      left: -100px;
    }}
    .content {{ position: relative; z-index: 1; }}
    .logo {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      font-size: 26px;
      font-weight: 800;
      color: {theme.accent};
      margin-bottom: 50px;
    }}
    .logo::before {{
      content: '';
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: {theme.gradient_primary};
    }}
    .headline {{
      font-size: 82px;
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -0.03em;
      max-width: 1000px;
      margin-bottom: 32px;
      background: {theme.gradient_primary};
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    .subhead {{
      font-size: 26px;
      color: {theme.text_secondary};
      max-width: 700px;
      line-height: 1.5;
      margin-bottom: 50px;
    }}
    .pills {{
      display: flex;
      gap: 16px;
    }}
    .pill {{
      background: {theme.surface};
      color: {theme.accent};
      padding: 12px 28px;
      border-radius: 50px;
      font-size: 15px;
      font-weight: 600;
      border: 2px solid {theme.border};
    }}
  </style>
</head>
<body>
  <div class="gradient-blob"></div>
  <div class="gradient-blob-2"></div>
  <div class="content">
    <div class="logo">{company_name}</div>
    <h1 class="headline">{headline.replace(chr(10), "<br>")}</h1>
    <p class="subhead">{subheadline}</p>
    <div class="pills">{bottom_items_html}</div>
  </div>
</body>
</html>'''

        # CREATIVE/AGENCY STYLE - Bold, asymmetric, accent bar
        elif 'creative' in style:
            bottom_items_html = "".join(
                f'<div class="meta-item">{item}</div>' for item in bottom_items
            )
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{company_name}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: grid;
      grid-template-columns: 100px 1fr;
    }}
    .accent-bar {{
      background: {theme.accent};
      display: flex;
      align-items: flex-end;
      padding-bottom: 80px;
      justify-content: center;
    }}
    .accent-bar span {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: {theme.background};
    }}
    .main {{
      padding: 100px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .company {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: {theme.accent};
      margin-bottom: 40px;
    }}
    .headline {{
      font-size: 96px;
      font-weight: 900;
      line-height: 0.95;
      letter-spacing: -0.04em;
      max-width: 1100px;
      margin-bottom: 40px;
    }}
    .subhead {{
      font-size: 24px;
      color: {theme.text_secondary};
      max-width: 650px;
      line-height: 1.5;
      margin-bottom: 60px;
      border-left: 4px solid {theme.accent};
      padding-left: 24px;
    }}
    .meta {{
      display: flex;
      gap: 48px;
    }}
    .meta-item {{
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: {theme.text_muted};
      padding: 12px 0;
      border-top: 2px solid {theme.border};
    }}
  </style>
</head>
<body>
  <div class="accent-bar"><span>{company_name}</span></div>
  <div class="main">
    <div class="company">{company_name}</div>
    <h1 class="headline">{headline.replace(chr(10), "<br>")}</h1>
    <p class="subhead">{subheadline}</p>
    <div class="meta">{bottom_items_html}</div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Extreme whitespace, sparse
        elif 'minimal' in style:
            bottom_html = " — ".join(bottom_items) if bottom_items else ""
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{company_name}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 140px 180px;
    }}
    .top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }}
    .company {{
      font-size: 15px;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: {theme.text_muted};
    }}
    .line {{
      flex: 1;
      height: 1px;
      background: {theme.border};
      margin: 0 60px;
      margin-top: 8px;
    }}
    .date {{
      font-size: 15px;
      color: {theme.text_muted};
    }}
    .center {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .headline {{
      font-size: 64px;
      font-weight: 300;
      line-height: 1.2;
      letter-spacing: -0.02em;
      max-width: 900px;
      margin-bottom: 40px;
    }}
    .subhead {{
      font-size: 20px;
      font-weight: 400;
      color: {theme.text_secondary};
      max-width: 600px;
      line-height: 1.7;
    }}
    .bottom {{
      font-size: 13px;
      color: {theme.text_muted};
    }}
  </style>
</head>
<body>
  <div class="top">
    <div class="company">{company_name}</div>
    <div class="line"></div>
    <div class="date">{bottom_items[0] if bottom_items else ""}</div>
  </div>
  <div class="center">
    <h1 class="headline">{headline.replace(chr(10), "<br>")}</h1>
    <p class="subhead">{subheadline}</p>
  </div>
  <div class="bottom">{bottom_html}</div>
</body>
</html>'''

        # SALES STYLE - Action-focused, benefit-driven
        elif 'sales' in style:
            benefits = bottom_items[:3] if len(bottom_items) >= 3 else bottom_items
            benefits_html = "".join(
                f'<div class="benefit"><span class="check">✓</span>{b}</div>' for b in benefits
            )
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{company_name}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: grid;
      grid-template-columns: 1fr 1fr;
    }}
    .left {{
      padding: 100px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .logo {{
      font-size: 22px;
      font-weight: 700;
      color: {theme.accent};
      margin-bottom: 50px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .logo::before {{
      content: '';
      width: 32px;
      height: 32px;
      background: {theme.accent};
      border-radius: 8px;
    }}
    .headline {{
      font-size: 68px;
      font-weight: 800;
      line-height: 1.05;
      letter-spacing: -0.03em;
      margin-bottom: 32px;
    }}
    .subhead {{
      font-size: 22px;
      color: {theme.text_secondary};
      line-height: 1.6;
      margin-bottom: 50px;
      max-width: 550px;
    }}
    .benefits {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .benefit {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 18px;
      font-weight: 500;
      color: {theme.text_secondary};
    }}
    .check {{
      width: 28px;
      height: 28px;
      background: {theme.accent};
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
    }}
    .right {{
      background: {theme.surface};
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }}
    .cta-box {{
      background: {theme.accent};
      color: white;
      padding: 60px;
      border-radius: 24px;
      text-align: center;
      max-width: 500px;
    }}
    .cta-title {{
      font-size: 32px;
      font-weight: 700;
      margin-bottom: 20px;
    }}
    .cta-sub {{
      font-size: 18px;
      opacity: 0.9;
      margin-bottom: 30px;
    }}
    .cta-btn {{
      display: inline-block;
      background: white;
      color: {theme.accent};
      padding: 16px 40px;
      border-radius: 8px;
      font-size: 16px;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="logo">{company_name}</div>
    <h1 class="headline">{headline.replace(chr(10), "<br>")}</h1>
    <p class="subhead">{subheadline}</p>
    <div class="benefits">{benefits_html}</div>
  </div>
  <div class="right">
    <div class="cta-box">
      <div class="cta-title">Ready to get started?</div>
      <div class="cta-sub">Join 500+ teams already using {company_name}</div>
      <div class="cta-btn">Start Free Trial →</div>
    </div>
  </div>
</body>
</html>'''

        # DEFAULT/TECH STYLE - Original design
        else:
            logo_html = ""
            if logo_url:
                logo_html = f'<img src="{logo_url}" alt="{company_name}" class="logo-img">'
            else:
                logo_html = f'<div class="logo">{company_name}</div>'

            bottom_items_html = "\n".join(
                f'<div class="bottom-item">{item}</div>' for item in bottom_items
            )

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{company_name} - Title</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 120px;
    }}
    .logo {{
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 60px;
      color: {theme.text_primary};
    }}
    .logo-img {{
      height: 40px;
      margin-bottom: 60px;
    }}
    .headline {{
      font-size: {theme.font_size_hero};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 40px;
      max-width: 1200px;
    }}
    .subhead {{
      font-size: {theme.font_size_subheadline};
      color: {theme.text_secondary};
      margin-bottom: 80px;
      max-width: 800px;
      line-height: {theme.line_height_normal};
    }}
    .bottom-row {{
      display: flex;
      gap: 60px;
      margin-top: auto;
    }}
    .bottom-item {{
      font-size: 16px;
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }}
  </style>
</head>
<body>
  {logo_html}
  <h1 class="headline">{headline}</h1>
  <p class="subhead">{subheadline}</p>
  <div class="bottom-row">
    {bottom_items_html}
  </div>
</body>
</html>'''

    @staticmethod
    def render_problem_slide(
        headline: str,
        story_html: str,
        label: Optional[str] = "Problem",
        product_box: Optional[Dict[str, Any]] = None,
        blocker_list: Optional[List[str]] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render problem/story slide with style-specific layouts.
        Pattern from: runit-pitch/slide-02-problem.html
        """
        theme = theme or LightTheme()
        blocker_list = blocker_list or []
        style = getattr(theme, 'name', 'light')

        # CONSULTING STYLE - Structured framework, numbered issues
        if 'consulting' in style:
            blockers_html = ""
            if blocker_list:
                items = "".join(f'''
                <div class="blocker-item">
                  <div class="blocker-num">{i+1}</div>
                  <div class="blocker-text">{item}</div>
                </div>''' for i, item in enumerate(blocker_list))
                blockers_html = f'''
                <div class="blockers-section">
                  <div class="section-title">Key Barriers</div>
                  {items}
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-bar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: {theme.accent};
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: {theme.accent};
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 24px;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 48px;
      font-weight: 600;
      line-height: 1.2;
      margin-bottom: 48px;
      max-width: 900px;
    }}
    .content-grid {{
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 80px;
      margin-top: 20px;
    }}
    .story {{
      font-size: 20px;
      line-height: 1.8;
      color: {theme.text_secondary};
      border-left: 3px solid {theme.accent};
      padding-left: 32px;
    }}
    .blockers-section {{
      background: {theme.surface};
      padding: 40px;
      border-radius: 4px;
    }}
    .section-title {{
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: {theme.text_muted};
      margin-bottom: 28px;
      padding-bottom: 16px;
      border-bottom: 1px solid {theme.border};
    }}
    .blocker-item {{
      display: flex;
      gap: 20px;
      margin-bottom: 24px;
    }}
    .blocker-num {{
      width: 32px;
      height: 32px;
      background: {theme.accent};
      color: white;
      border-radius: 2px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 14px;
      flex-shrink: 0;
    }}
    .blocker-text {{
      font-size: 17px;
      line-height: 1.5;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="content-grid">
    <div class="story">{story_html}</div>
    {blockers_html}
  </div>
</body>
</html>'''

        # CONSUMER STYLE - Playful, emoji icons, rounded cards
        elif 'consumer' in style:
            blockers_html = ""
            if blocker_list:
                icons = ["😤", "😩", "🤯", "😵"]
                items = "".join(f'''
                <div class="blocker-card">
                  <div class="blocker-icon">{icons[i % len(icons)]}</div>
                  <div class="blocker-text">{item}</div>
                </div>''' for i, item in enumerate(blocker_list))
                blockers_html = f'<div class="blockers-grid">{items}</div>'

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .gradient-blob {{
      position: absolute;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      background: {theme.gradient_primary};
      opacity: 0.1;
      filter: blur(80px);
      bottom: -200px;
      left: -100px;
    }}
    .label {{
      display: inline-block;
      background: {theme.accent};
      color: white;
      padding: 8px 20px;
      border-radius: 100px;
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 56px;
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 40px;
      background: {theme.gradient_text};
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      max-width: 800px;
    }}
    .story {{
      font-size: 22px;
      line-height: 1.8;
      color: {theme.text_secondary};
      max-width: 700px;
      margin-bottom: 50px;
    }}
    .blockers-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
    }}
    .blocker-card {{
      background: {theme.surface};
      padding: 32px 24px;
      border-radius: 24px;
      text-align: center;
      border: 2px solid {theme.border};
    }}
    .blocker-icon {{
      font-size: 48px;
      margin-bottom: 16px;
    }}
    .blocker-text {{
      font-size: 16px;
      line-height: 1.5;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="gradient-blob"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="story">{story_html}</div>
  {blockers_html}
</body>
</html>'''

        # CREATIVE STYLE - Bold asymmetric, large typography
        elif 'creative' in style:
            blockers_html = ""
            if blocker_list:
                items = "".join(f'''
                <div class="blocker-row">
                  <span class="x-mark">×</span>
                  <span>{item}</span>
                </div>''' for item in blocker_list)
                blockers_html = f'<div class="blockers-list">{items}</div>'

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: grid;
      grid-template-columns: 100px 1fr;
    }}
    .sidebar {{
      background: {theme.accent};
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: {theme.background};
    }}
    .main {{
      padding: 80px 100px;
      display: flex;
      flex-direction: column;
    }}
    .headline {{
      font-size: 72px;
      font-weight: 900;
      line-height: 1.05;
      margin-bottom: 48px;
      max-width: 900px;
    }}
    .content-row {{
      display: flex;
      gap: 80px;
      flex: 1;
      align-items: flex-start;
    }}
    .story {{
      flex: 1.2;
      font-size: 22px;
      line-height: 1.8;
      color: {theme.text_secondary};
    }}
    .blockers-list {{
      flex: 1;
      padding-top: 8px;
    }}
    .blocker-row {{
      display: flex;
      gap: 20px;
      font-size: 20px;
      padding: 20px 0;
      border-bottom: 1px solid {theme.border_light};
      color: {theme.text_secondary};
    }}
    .x-mark {{
      color: {theme.accent};
      font-size: 28px;
      font-weight: 900;
    }}
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-text">{label}</div>
  </div>
  <div class="main">
    <h1 class="headline">{headline}</h1>
    <div class="content-row">
      <div class="story">{story_html}</div>
      {blockers_html}
    </div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Maximum whitespace, subtle
        elif 'minimal' in style:
            blockers_html = ""
            if blocker_list:
                items = "".join(f'<li>{item}</li>' for item in blocker_list)
                blockers_html = f'<ul class="blockers">{items}</ul>'

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
    }}
    .label {{
      font-size: 11px;
      font-weight: 500;
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.2em;
      margin-bottom: 60px;
    }}
    .headline {{
      font-size: 44px;
      font-weight: 400;
      line-height: 1.3;
      margin-bottom: 80px;
      max-width: 900px;
      letter-spacing: -0.02em;
    }}
    .content {{
      display: flex;
      gap: 120px;
    }}
    .story {{
      flex: 1;
      font-size: 18px;
      font-weight: 300;
      line-height: 2;
      color: {theme.text_secondary};
    }}
    .blockers {{
      flex: 1;
      list-style: none;
    }}
    .blockers li {{
      font-size: 17px;
      font-weight: 400;
      color: {theme.text_secondary};
      padding: 20px 0;
      border-bottom: 1px solid {theme.border_light};
    }}
    .blockers li:last-child {{
      border-bottom: none;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="content">
    <div class="story">{story_html}</div>
    {blockers_html}
  </div>
</body>
</html>'''

        # SALES STYLE - Dramatic split, high contrast
        elif 'sales' in style:
            blockers_html = ""
            if blocker_list:
                items = "".join(f'''
                <div class="blocker-item">
                  <div class="blocker-bullet"></div>
                  <div>{item}</div>
                </div>''' for item in blocker_list)
                blockers_html = f'''
                <div class="blockers-box">
                  <div class="blockers-title">The Real Blockers</div>
                  {items}
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .left {{
      flex: 1.3;
      padding: 80px 60px 80px 100px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .right {{
      flex: 1;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      color: white;
      padding: 80px 60px;
      display: flex;
      align-items: center;
    }}
    .label {{
      display: inline-block;
      background: #fef2f2;
      color: #dc2626;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 40px;
    }}
    .story {{
      font-size: 20px;
      line-height: 1.8;
      color: {theme.text_secondary};
    }}
    .blockers-box {{
      width: 100%;
    }}
    .blockers-title {{
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: rgba(255,255,255,0.5);
      margin-bottom: 32px;
    }}
    .blocker-item {{
      display: flex;
      gap: 20px;
      padding: 24px 0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      font-size: 18px;
      line-height: 1.5;
    }}
    .blocker-bullet {{
      width: 10px;
      height: 10px;
      background: {theme.accent};
      border-radius: 50%;
      margin-top: 8px;
      flex-shrink: 0;
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="story">{story_html}</div>
  </div>
  <div class="right">
    {blockers_html}
  </div>
</body>
</html>'''

        # DEFAULT/TECH STYLE - Original two-column layout
        blockers_html = ""
        if blocker_list:
            items = "\n".join(f'<li>{item}</li>' for item in blocker_list)
            blockers_html = f'''
            <div class="blockers">
              <div class="blockers-title">Why hasn't this been solved?</div>
              <ul class="blocker-list">{items}</ul>
            </div>'''

        product_html = ""
        if product_box:
            product_html = f'''
            <div class="product-box">
              <div class="product-title">{product_box.get("title", "")}</div>
              <div class="product-desc">{product_box.get("description", "")}</div>
            </div>'''

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      padding: {theme.slide_padding};
    }}
    .left {{
      flex: 1.3;
      display: flex;
      flex-direction: column;
      padding-right: 80px;
    }}
    .right {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 40px;
    }}
    .story {{
      font-size: 22px;
      line-height: 1.7;
      color: {theme.text_secondary};
    }}
    .story strong {{
      color: {theme.text_primary};
      font-weight: {theme.font_weight_semibold};
    }}
    .product-box {{
      background: {theme.surface};
      padding: 40px;
      border-radius: {theme.radius_large};
      margin-bottom: 32px;
    }}
    .product-title {{
      font-size: 24px;
      font-weight: {theme.font_weight_bold};
      margin-bottom: 16px;
    }}
    .product-desc {{
      font-size: 18px;
      color: {theme.text_secondary};
      line-height: 1.6;
    }}
    .blockers {{
      padding: 32px;
      background: {theme.surface};
      border-radius: {theme.radius_medium};
    }}
    .blockers-title {{
      font-size: 18px;
      font-weight: {theme.font_weight_semibold};
      margin-bottom: 16px;
    }}
    .blocker-list {{
      list-style: none;
    }}
    .blocker-list li {{
      font-size: 18px;
      color: {theme.text_secondary};
      padding: 8px 0;
      padding-left: 24px;
      position: relative;
    }}
    .blocker-list li::before {{
      content: "×";
      position: absolute;
      left: 0;
      color: #e11d48;
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="story">{story_html}</div>
  </div>
  <div class="right">
    {product_html}
    {blockers_html}
  </div>
</body>
</html>'''

    @staticmethod
    def render_validation_slide(
        headline: str,
        quotes: List[Dict[str, str]],
        label: Optional[str] = "Validation",
        bottom_stat: Optional[Dict[str, str]] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render validation/quotes grid slide with style-specific layouts.
        quotes: List of {quote, author, role, emphasis (optional list of strings to highlight)}
        bottom_stat: {number, text}
        """
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        def format_quote(q: Dict) -> str:
            text = q.get("quote", "")
            emphasis = q.get("emphasis", [])
            for emp in emphasis:
                text = text.replace(emp, f"<em>{emp}</em>")
            return text

        def get_initials(name: str) -> str:
            parts = name.split()
            return parts[0][0].upper() if parts else "?"

        # CONSULTING STYLE - Structured testimonials with border
        if 'consulting' in style:
            quotes_html = "".join(f'''
            <div class="quote-card">
              <div class="quote-mark">"</div>
              <div class="quote-text">{format_quote(q)}</div>
              <div class="quote-author">
                <div class="author-name">{q.get("author", "")}</div>
                <div class="author-role">{q.get("role", "")}</div>
              </div>
            </div>''' for q in quotes[:4])

            bottom_html = ""
            if bottom_stat:
                bottom_html = f'''
            <div class="bottom-stat">
              <span class="stat-num">{bottom_stat.get("number", "")}</span>
              <span class="stat-text">{bottom_stat.get("text", "")}</span>
            </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-bar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: {theme.accent};
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: {theme.accent};
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 24px;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 48px;
      font-weight: 600;
      margin-bottom: 50px;
    }}
    .quotes-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 32px;
    }}
    .quote-card {{
      background: {theme.surface};
      padding: 36px;
      border-left: 4px solid {theme.accent};
    }}
    .quote-mark {{
      font-family: {theme.headline_font_family};
      font-size: 60px;
      color: {theme.accent};
      line-height: 0.5;
      margin-bottom: 16px;
    }}
    .quote-text {{
      font-size: 18px;
      line-height: 1.7;
      color: {theme.text_secondary};
      margin-bottom: 24px;
      font-style: italic;
    }}
    .quote-text em {{
      background: rgba(74, 144, 217, 0.15);
      padding: 2px 4px;
      font-style: italic;
    }}
    .author-name {{
      font-size: 15px;
      font-weight: 600;
      color: {theme.text_primary};
    }}
    .author-role {{
      font-size: 13px;
      color: {theme.text_muted};
      margin-top: 4px;
    }}
    .bottom-stat {{
      margin-top: 40px;
      padding: 24px 32px;
      background: {theme.accent};
      color: white;
      display: flex;
      align-items: center;
      gap: 20px;
    }}
    .stat-num {{
      font-size: 36px;
      font-weight: 700;
    }}
    .stat-text {{
      font-size: 18px;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="quotes-grid">
    {quotes_html}
  </div>
  {bottom_html}
</body>
</html>'''

        # CONSUMER STYLE - Fun testimonials with avatars
        elif 'consumer' in style:
            quotes_html = "".join(f'''
            <div class="quote-card">
              <div class="stars">★★★★★</div>
              <div class="quote-text">"{format_quote(q)}"</div>
              <div class="quote-author">
                <div class="author-avatar">{get_initials(q.get("author", ""))}</div>
                <div class="author-info">
                  <div class="author-name">{q.get("author", "")}</div>
                  <div class="author-role">{q.get("role", "")}</div>
                </div>
              </div>
            </div>''' for q in quotes[:4])

            bottom_html = ""
            if bottom_stat:
                bottom_html = f'''
            <div class="bottom-stat">
              <span class="stat-num">{bottom_stat.get("number", "")}</span>
              <span class="stat-text">{bottom_stat.get("text", "")}</span>
            </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .gradient-blob {{
      position: absolute;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      background: {theme.gradient_primary};
      opacity: 0.1;
      filter: blur(80px);
      bottom: -150px;
      right: -150px;
    }}
    .label {{
      display: inline-block;
      background: {theme.accent};
      color: white;
      padding: 8px 20px;
      border-radius: 100px;
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      margin-bottom: 50px;
      background: {theme.gradient_text};
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .quotes-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 28px;
    }}
    .quote-card {{
      background: {theme.surface};
      border-radius: 24px;
      padding: 32px;
      border: 2px solid {theme.border};
    }}
    .stars {{
      color: {theme.accent};
      font-size: 20px;
      margin-bottom: 16px;
    }}
    .quote-text {{
      font-size: 18px;
      line-height: 1.6;
      color: {theme.text_primary};
      margin-bottom: 24px;
    }}
    .quote-text em {{
      background: rgba(236, 72, 153, 0.15);
      padding: 2px 4px;
      font-style: normal;
    }}
    .quote-author {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .author-avatar {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: {theme.accent};
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
    }}
    .author-name {{
      font-size: 15px;
      font-weight: 600;
    }}
    .author-role {{
      font-size: 13px;
      color: {theme.text_muted};
    }}
    .bottom-stat {{
      margin-top: 32px;
      padding: 24px 32px;
      background: {theme.gradient_primary};
      color: white;
      border-radius: 16px;
      display: flex;
      align-items: center;
      gap: 20px;
    }}
    .stat-num {{
      font-size: 40px;
      font-weight: 800;
    }}
    .stat-text {{
      font-size: 18px;
    }}
  </style>
</head>
<body>
  <div class="gradient-blob"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="quotes-grid">
    {quotes_html}
  </div>
  {bottom_html}
</body>
</html>'''

        # CREATIVE STYLE - Bold asymmetric quotes
        elif 'creative' in style:
            quotes_html = "".join(f'''
            <div class="quote-card">
              <div class="quote-text">"{format_quote(q)}"</div>
              <div class="author-line">— {q.get("author", "")}, {q.get("role", "")}</div>
            </div>''' for q in quotes[:4])

            bottom_html = ""
            if bottom_stat:
                bottom_html = f'''
            <div class="bottom-stat">
              <span class="stat-num">{bottom_stat.get("number", "")}</span>
              <span class="stat-text">{bottom_stat.get("text", "")}</span>
            </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: grid;
      grid-template-columns: 100px 1fr;
    }}
    .sidebar {{
      background: {theme.accent};
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: {theme.background};
    }}
    .main {{
      padding: 80px 100px;
    }}
    .headline {{
      font-size: 64px;
      font-weight: 900;
      margin-bottom: 50px;
    }}
    .quotes-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 40px;
    }}
    .quote-card {{
      border-left: 5px solid {theme.accent};
      padding-left: 28px;
    }}
    .quote-text {{
      font-size: 20px;
      line-height: 1.6;
      margin-bottom: 16px;
    }}
    .quote-text em {{
      background: rgba(250, 204, 21, 0.3);
      padding: 2px 4px;
      font-style: normal;
    }}
    .author-line {{
      font-size: 15px;
      color: {theme.text_muted};
    }}
    .bottom-stat {{
      margin-top: 40px;
      padding: 24px 32px;
      background: {theme.accent};
      color: {theme.background};
      display: flex;
      align-items: center;
      gap: 20px;
    }}
    .stat-num {{
      font-size: 40px;
      font-weight: 900;
    }}
    .stat-text {{
      font-size: 18px;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-text">{label}</div>
  </div>
  <div class="main">
    <h1 class="headline">{headline}</h1>
    <div class="quotes-grid">
      {quotes_html}
    </div>
    {bottom_html}
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Simple elegant quotes
        elif 'minimal' in style:
            quotes_html = "".join(f'''
            <div class="quote-card">
              <div class="quote-text">"{format_quote(q)}"</div>
              <div class="author-line">{q.get("author", "")} · {q.get("role", "")}</div>
            </div>''' for q in quotes[:4])

            bottom_html = ""
            if bottom_stat:
                bottom_html = f'''
            <div class="bottom-stat">
              <span class="stat-num">{bottom_stat.get("number", "")}</span>
              <span class="stat-text">{bottom_stat.get("text", "")}</span>
            </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
    }}
    .label {{
      font-size: 11px;
      font-weight: 500;
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.2em;
      margin-bottom: 48px;
    }}
    .headline {{
      font-size: 40px;
      font-weight: 400;
      margin-bottom: 60px;
      letter-spacing: -0.02em;
    }}
    .quotes-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 60px 80px;
    }}
    .quote-card {{
    }}
    .quote-text {{
      font-size: 18px;
      font-weight: 300;
      line-height: 1.8;
      margin-bottom: 20px;
      color: {theme.text_secondary};
    }}
    .quote-text em {{
      font-weight: 500;
      font-style: normal;
    }}
    .author-line {{
      font-size: 14px;
      color: {theme.text_muted};
    }}
    .bottom-stat {{
      margin-top: 60px;
      display: flex;
      align-items: baseline;
      gap: 16px;
    }}
    .stat-num {{
      font-size: 48px;
      font-weight: 300;
    }}
    .stat-text {{
      font-size: 16px;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="quotes-grid">
    {quotes_html}
  </div>
  {bottom_html}
</body>
</html>'''

        # SALES STYLE - Testimonials with trust signals
        elif 'sales' in style:
            quotes_html = "".join(f'''
            <div class="quote-card">
              <div class="quote-text">"{format_quote(q)}"</div>
              <div class="quote-author">
                <div class="author-avatar">{get_initials(q.get("author", ""))}</div>
                <div class="author-info">
                  <div class="author-name">{q.get("author", "")}</div>
                  <div class="author-role">{q.get("role", "")}</div>
                </div>
                <div class="verified">✓ Verified</div>
              </div>
            </div>''' for q in quotes[:4])

            bottom_html = ""
            if bottom_stat:
                bottom_html = f'''
            <div class="bottom-stat">
              <span class="stat-num">{bottom_stat.get("number", "")}</span>
              <span class="stat-text">{bottom_stat.get("text", "")}</span>
            </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .label {{
      display: inline-block;
      background: #fef3c7;
      color: #92400e;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 48px;
      font-weight: 800;
      margin-bottom: 50px;
    }}
    .quotes-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 28px;
    }}
    .quote-card {{
      background: {theme.surface};
      border-radius: 16px;
      padding: 32px;
      border: 1px solid {theme.border};
    }}
    .quote-text {{
      font-size: 18px;
      line-height: 1.6;
      margin-bottom: 24px;
    }}
    .quote-text em {{
      background: #dcfce7;
      padding: 2px 4px;
      font-style: normal;
    }}
    .quote-author {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .author-avatar {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: {theme.accent};
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
    }}
    .author-info {{
      flex: 1;
    }}
    .author-name {{
      font-size: 15px;
      font-weight: 600;
    }}
    .author-role {{
      font-size: 13px;
      color: {theme.text_muted};
    }}
    .verified {{
      font-size: 12px;
      color: #059669;
      background: #ecfdf5;
      padding: 4px 10px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .bottom-stat {{
      margin-top: 32px;
      padding: 24px 32px;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      color: white;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 20px;
    }}
    .stat-num {{
      font-size: 40px;
      font-weight: 800;
      color: {theme.accent};
    }}
    .stat-text {{
      font-size: 18px;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="quotes-grid">
    {quotes_html}
  </div>
  {bottom_html}
</body>
</html>'''

        # DEFAULT/TECH STYLE - Original 2x2 grid
        quotes_html = "\n".join(f'''
        <div class="quote-card">
          <div class="quote-text">"{format_quote(q)}"</div>
          <div class="quote-author">
            <div class="author-avatar">{get_initials(q.get("author", ""))}</div>
            <div class="author-info">
              <div class="author-name">{q.get("author", "")}</div>
              <div class="author-role">{q.get("role", "")}</div>
            </div>
          </div>
        </div>''' for q in quotes[:4])

        bottom_html = ""
        if bottom_stat:
            bottom_html = f'''
        <div class="bottom-note">
          <div class="bottom-note-number">{bottom_stat.get("number", "")}</div>
          <div>{bottom_stat.get("text", "")}</div>
        </div>'''

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: {theme.font_weight_extrabold};
      line-height: 1.15;
      letter-spacing: {theme.letter_spacing_tight};
      color: {theme.text_primary};
      margin-bottom: 60px;
    }}
    .quotes-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 40px;
      flex: 1;
    }}
    .quote-card {{
      background: {theme.surface};
      border-radius: {theme.radius_large};
      padding: 40px;
      display: flex;
      flex-direction: column;
    }}
    .quote-text {{
      font-size: 22px;
      line-height: 1.6;
      color: {theme.text_primary};
      margin-bottom: 32px;
      flex: 1;
    }}
    .quote-text em {{
      background: #fff3cd;
      padding: 2px 6px;
      font-style: normal;
    }}
    .quote-author {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .author-avatar {{
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: {theme.border};
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: {theme.font_weight_bold};
      font-size: 18px;
      color: {theme.text_muted};
    }}
    .author-info {{
      display: flex;
      flex-direction: column;
    }}
    .author-name {{
      font-size: 16px;
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_primary};
    }}
    .author-role {{
      font-size: 14px;
      color: {theme.text_muted};
    }}
    .bottom-note {{
      margin-top: 40px;
      padding: 24px 32px;
      background: #000;
      color: #fff;
      border-radius: {theme.radius_medium};
      font-size: 20px;
      display: flex;
      align-items: center;
      gap: 24px;
    }}
    .bottom-note-number {{
      font-size: 48px;
      font-weight: {theme.font_weight_extrabold};
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="quotes-grid">
    {quotes_html}
  </div>
  {bottom_html}
</body>
</html>'''

    @staticmethod
    def render_market_slide(
        headline: str,
        tam: Dict[str, str],
        sam: Dict[str, str],
        som: Dict[str, str],
        segments: Optional[List[Dict[str, Any]]] = None,
        label: Optional[str] = "Market",
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render market sizing slide with style-specific layouts.
        tam/sam/som: {value, description}
        segments: List of {title, items: List[str]}
        """
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')
        segments = segments or []

        # =====================================================================
        # CONSULTING STYLE - Professional nested boxes
        # =====================================================================
        if 'consulting' in style:
            segments_html = ""
            if segments:
                seg_items = "".join(f'<div class="seg-card"><div class="seg-title">{s.get("title","")}</div><ul>{"".join(f"<li>{i}</li>" for i in s.get("items",[]))}</ul></div>' for s in segments[:3])
                segments_html = f'<div class="segments">{seg_items}</div>'

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Source Sans Pro', sans-serif; background: #fff; color: #1a2744; width: 1920px; height: 1080px; padding: 80px 100px; }}
    .top-bar {{ width: 100%; height: 8px; background: #1a2744; position: absolute; top: 0; left: 0; }}
    .label {{ font-size: 12px; font-weight: 600; color: #4a90d9; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; }}
    .headline {{ font-family: {theme.headline_font_family}; font-size: 48px; font-weight: 700; margin-bottom: 50px; }}
    .market-boxes {{ display: flex; gap: 40px; margin-bottom: 50px; }}
    .box {{ flex: 1; padding: 32px; border: 2px solid #e8ecf2; }}
    .box.som {{ background: #1a2744; color: white; border-color: #1a2744; }}
    .box-label {{ font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #4a90d9; margin-bottom: 12px; }}
    .box.som .box-label {{ color: #6ba3e0; }}
    .box-value {{ font-size: 48px; font-weight: 700; margin-bottom: 12px; }}
    .box-desc {{ font-size: 16px; color: #3d5a80; line-height: 1.5; }}
    .box.som .box-desc {{ color: rgba(255,255,255,0.7); }}
    .segments {{ display: flex; gap: 32px; }}
    .seg-card {{ flex: 1; background: #f5f7fa; padding: 28px; }}
    .seg-title {{ font-size: 16px; font-weight: 600; color: #1a2744; margin-bottom: 16px; }}
    .seg-card ul {{ list-style: none; }}
    .seg-card li {{ font-size: 15px; color: #3d5a80; padding: 8px 0; border-bottom: 1px solid #e8ecf2; }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="market-boxes">
    <div class="box"><div class="box-label">TAM</div><div class="box-value">{tam.get("value","")}</div><div class="box-desc">{tam.get("description","")}</div></div>
    <div class="box"><div class="box-label">SAM</div><div class="box-value">{sam.get("value","")}</div><div class="box-desc">{sam.get("description","")}</div></div>
    <div class="box som"><div class="box-label">SOM (Year 1)</div><div class="box-value">{som.get("value","")}</div><div class="box-desc">{som.get("description","")}</div></div>
  </div>
  {segments_html}
</body>
</html>'''

        # =====================================================================
        # CONSUMER STYLE - Colorful gradient cards
        # =====================================================================
        elif 'consumer' in style:
            segments_html = ""
            if segments:
                seg_items = "".join(f'<div class="seg"><div class="seg-title">{s.get("title","")}</div>{"".join(f"<div class=seg-item>→ {i}</div>" for i in s.get("items",[]))}</div>' for s in segments[:3])
                segments_html = f'<div class="segments">{seg_items}</div>'

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: linear-gradient(180deg, #fffbfc 0%, #fdf2f8 100%); color: #1f1f1f; width: 1920px; height: 1080px; padding: 80px 100px; position: relative; overflow: hidden; }}
    .blob {{ position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.4; }}
    .blob-1 {{ width: 400px; height: 400px; background: #ec4899; top: -100px; right: 200px; }}
    .main {{ position: relative; z-index: 1; }}
    .label {{ display: inline-block; background: linear-gradient(135deg, #ec4899, #a855f7); color: white; font-size: 13px; font-weight: 700; padding: 8px 20px; border-radius: 50px; margin-bottom: 24px; }}
    .headline {{ font-size: 52px; font-weight: 800; margin-bottom: 40px; }}
    .boxes {{ display: flex; gap: 28px; margin-bottom: 40px; }}
    .box {{ flex: 1; background: white; border-radius: 24px; padding: 32px; box-shadow: 0 4px 24px rgba(236,72,153,0.1); }}
    .box.som {{ background: linear-gradient(135deg, #ec4899, #db2777); color: white; }}
    .box-label {{ font-size: 12px; font-weight: 700; text-transform: uppercase; opacity: 0.6; margin-bottom: 12px; }}
    .box-value {{ font-size: 48px; font-weight: 800; background: linear-gradient(135deg, #ec4899, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .box.som .box-value {{ background: none; -webkit-text-fill-color: white; }}
    .box-desc {{ font-size: 16px; color: #666; margin-top: 12px; }}
    .box.som .box-desc {{ color: rgba(255,255,255,0.8); }}
    .segments {{ display: flex; gap: 24px; }}
    .seg {{ flex: 1; background: white; border-radius: 20px; padding: 28px; box-shadow: 0 4px 20px rgba(236,72,153,0.08); }}
    .seg-title {{ font-size: 18px; font-weight: 700; color: #ec4899; margin-bottom: 16px; }}
    .seg-item {{ font-size: 15px; color: #666; padding: 8px 0; }}
  </style>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="main">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="boxes">
      <div class="box"><div class="box-label">TAM</div><div class="box-value">{tam.get("value","")}</div><div class="box-desc">{tam.get("description","")}</div></div>
      <div class="box"><div class="box-label">SAM</div><div class="box-value">{sam.get("value","")}</div><div class="box-desc">{sam.get("description","")}</div></div>
      <div class="box som"><div class="box-label">SOM (Year 1)</div><div class="box-value">{som.get("value","")}</div><div class="box-desc">{som.get("description","")}</div></div>
    </div>
    {segments_html}
  </div>
</body>
</html>'''

        # =====================================================================
        # CREATIVE STYLE - Bold asymmetric
        # =====================================================================
        elif 'creative' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: #0f0f0f; color: #f5f5f5; width: 1920px; height: 1080px; display: flex; }}
    .sidebar {{ width: 100px; background: #facc15; display: flex; align-items: center; justify-content: center; }}
    .sidebar-text {{ writing-mode: vertical-rl; transform: rotate(180deg); font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 4px; color: #0f0f0f; }}
    .main {{ flex: 1; padding: 80px; }}
    .label {{ font-size: 13px; font-weight: 800; color: #facc15; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 24px; }}
    .headline {{ font-size: 60px; font-weight: 900; line-height: 1.0; margin-bottom: 60px; }}
    .boxes {{ display: flex; gap: 32px; }}
    .box {{ flex: 1; background: #1a1a1a; padding: 40px; }}
    .box.som {{ background: #facc15; color: #0f0f0f; }}
    .box-label {{ font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; opacity: 0.5; margin-bottom: 16px; }}
    .box-value {{ font-size: 56px; font-weight: 900; color: #facc15; }}
    .box.som .box-value {{ color: #0f0f0f; }}
    .box-desc {{ font-size: 16px; margin-top: 16px; opacity: 0.7; line-height: 1.5; }}
  </style>
</head>
<body>
  <div class="sidebar"><span class="sidebar-text">Market Size</span></div>
  <div class="main">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="boxes">
      <div class="box"><div class="box-label">TAM</div><div class="box-value">{tam.get("value","")}</div><div class="box-desc">{tam.get("description","")}</div></div>
      <div class="box"><div class="box-label">SAM</div><div class="box-value">{sam.get("value","")}</div><div class="box-desc">{sam.get("description","")}</div></div>
      <div class="box som"><div class="box-label">SOM</div><div class="box-value">{som.get("value","")}</div><div class="box-desc">{som.get("description","")}</div></div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # MINIMAL STYLE - Clean whitespace
        # =====================================================================
        elif 'minimal' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: #fafafa; color: #171717; width: 1920px; height: 1080px; padding: 120px 160px; }}
    .label {{ font-size: 12px; font-weight: 500; color: #a3a3a3; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 32px; }}
    .headline {{ font-size: 44px; font-weight: 300; letter-spacing: -0.02em; margin-bottom: 80px; }}
    .boxes {{ display: flex; gap: 1px; background: #e5e5e5; }}
    .box {{ flex: 1; background: #fafafa; padding: 48px; }}
    .box.som {{ background: #171717; color: #fafafa; }}
    .box-label {{ font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; color: #a3a3a3; margin-bottom: 20px; }}
    .box.som .box-label {{ color: #737373; }}
    .box-value {{ font-size: 48px; font-weight: 500; margin-bottom: 16px; }}
    .box-desc {{ font-size: 15px; color: #737373; line-height: 1.6; }}
    .box.som .box-desc {{ color: #a3a3a3; }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="boxes">
    <div class="box"><div class="box-label">TAM</div><div class="box-value">{tam.get("value","")}</div><div class="box-desc">{tam.get("description","")}</div></div>
    <div class="box"><div class="box-label">SAM</div><div class="box-value">{sam.get("value","")}</div><div class="box-desc">{sam.get("description","")}</div></div>
    <div class="box som"><div class="box-label">SOM</div><div class="box-value">{som.get("value","")}</div><div class="box-desc">{som.get("description","")}</div></div>
  </div>
</body>
</html>'''

        # =====================================================================
        # SALES STYLE - Growth focused
        # =====================================================================
        elif 'sales' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: #0c1929; color: #fff; width: 1920px; height: 1080px; padding: 80px 100px; }}
    .label {{ font-size: 13px; font-weight: 700; color: #10b981; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; }}
    .headline {{ font-size: 52px; font-weight: 800; margin-bottom: 50px; }}
    .boxes {{ display: flex; gap: 28px; }}
    .box {{ flex: 1; background: #132337; border-radius: 16px; padding: 36px; }}
    .box.som {{ background: linear-gradient(135deg, #132337, #1a3a4f); border: 2px solid #10b981; }}
    .box-label {{ font-size: 12px; font-weight: 700; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 16px; }}
    .box-value {{ font-size: 48px; font-weight: 800; color: #10b981; }}
    .box-desc {{ font-size: 16px; color: rgba(255,255,255,0.6); margin-top: 16px; line-height: 1.5; }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="boxes">
    <div class="box"><div class="box-label">TAM</div><div class="box-value">{tam.get("value","")}</div><div class="box-desc">{tam.get("description","")}</div></div>
    <div class="box"><div class="box-label">SAM</div><div class="box-value">{sam.get("value","")}</div><div class="box-desc">{sam.get("description","")}</div></div>
    <div class="box som"><div class="box-label">SOM (Year 1)</div><div class="box-value">{som.get("value","")}</div><div class="box-desc">{som.get("description","")}</div></div>
  </div>
</body>
</html>'''

        # =====================================================================
        # DEFAULT/TECH STYLE
        # =====================================================================
        segments_html = ""
        if segments:
            segment_cards = "\n".join(f'''
            <div class="segment">
              <div class="segment-title">{seg.get("title", "")}</div>
              <ul class="segment-list">
                {"".join(f'<li>{item}</li>' for item in seg.get("items", []))}
              </ul>
            </div>''' for seg in segments[:3])
            segments_html = f'<div class="segments">{segment_cards}</div>'

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.font_family}; background: {theme.background}; width: 1920px; height: 1080px; display: flex; flex-direction: column; padding: {theme.slide_padding}; }}
    .slide-label {{ font-size: {theme.font_size_label}; font-weight: {theme.font_weight_semibold}; color: {theme.text_muted}; text-transform: uppercase; letter-spacing: {theme.letter_spacing_wide}; margin-bottom: 40px; }}
    .headline {{ font-size: {theme.font_size_headline}; font-weight: {theme.font_weight_bold}; line-height: 1.2; color: {theme.text_primary}; margin-bottom: 60px; }}
    .market-row {{ display: flex; gap: 60px; margin-bottom: 60px; }}
    .market-box {{ flex: 1; padding: 40px; border-radius: {theme.radius_medium}; }}
    .market-box.tam {{ background: #f5f5f5; }}
    .market-box.sam {{ background: #e8e8e8; }}
    .market-box.som {{ background: #000; color: #fff; }}
    .market-label {{ font-size: {theme.font_size_label}; font-weight: {theme.font_weight_semibold}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px; opacity: 0.6; }}
    .market-number {{ font-size: 64px; font-weight: {theme.font_weight_bold}; margin-bottom: 16px; }}
    .market-desc {{ font-size: 20px; line-height: {theme.line_height_normal}; opacity: 0.8; }}
    .market-box.som .market-label, .market-box.som .market-desc {{ color: rgba(255,255,255,0.7); }}
    .segments {{ display: flex; gap: 40px; flex: 1; }}
    .segment {{ flex: 1; padding: 32px; background: {theme.surface}; border-radius: {theme.radius_medium}; }}
    .segment-title {{ font-size: 20px; font-weight: {theme.font_weight_semibold}; color: {theme.text_primary}; margin-bottom: 16px; }}
    .segment-list {{ list-style: none; display: flex; flex-direction: column; gap: 12px; }}
    .segment-list li {{ font-size: 18px; color: {theme.text_secondary}; padding-left: 20px; position: relative; }}
    .segment-list li::before {{ content: "→"; position: absolute; left: 0; color: {theme.text_muted}; }}
  </style>
</head>
<body>
  <div class="slide-label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="market-row">
    <div class="market-box tam"><div class="market-label">TAM</div><div class="market-number">{tam.get("value", "")}</div><div class="market-desc">{tam.get("description", "")}</div></div>
    <div class="market-box sam"><div class="market-label">SAM</div><div class="market-number">{sam.get("value", "")}</div><div class="market-desc">{sam.get("description", "")}</div></div>
    <div class="market-box som"><div class="market-label">SOM (Year 1)</div><div class="market-number">{som.get("value", "")}</div><div class="market-desc">{som.get("description", "")}</div></div>
  </div>
  {segments_html}
</body>
</html>'''

    @staticmethod
    def render_team_ask_slide(
        founder_name: str,
        founder_title: str,
        bio_items: List[Dict[str, str]],
        ask_amount: str,
        ask_uses: List[str],
        founder_photo: Optional[str] = None,
        contact_info: Optional[Dict[str, str]] = None,
        looking_for: Optional[Dict[str, str]] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render team & ask slide with style-specific layouts.
        bio_items: List of {company, detail}
        contact_info: {email, linkedin}
        looking_for: {title, text}
        """
        theme = theme or DarkTheme()
        contact_info = contact_info or {}
        style = getattr(theme, 'name', 'dark')

        bio_html = "\n".join(f'''
        <div class="bio-item">
          <span class="company">{item.get("company", "")}</span>
          <span class="detail">{item.get("detail", "")}</span>
        </div>''' for item in bio_items)

        uses_html = "<br>".join(f"• {use}" for use in ask_uses)

        # CONSULTING STYLE - Formal, centered, minimal
        if 'consulting' in style:
            contact_lines = []
            if contact_info.get("email"):
                contact_lines.append(contact_info["email"])
            if contact_info.get("linkedin"):
                contact_lines.append(contact_info["linkedin"])
            contact_html = " · ".join(contact_lines) if contact_lines else ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Team & Ask</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}
    .top-bar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 8px;
      background: {theme.accent};
    }}
    .name {{
      font-family: {theme.headline_font_family};
      font-size: 64px;
      font-weight: 600;
      margin-bottom: 16px;
    }}
    .title-text {{
      font-size: 24px;
      color: {theme.text_secondary};
      margin-bottom: 48px;
    }}
    .divider {{
      width: 100px;
      height: 2px;
      background: {theme.accent};
      margin: 0 auto 48px;
    }}
    .ask-section {{
      background: {theme.surface};
      padding: 48px 80px;
      margin-bottom: 40px;
    }}
    .ask-label {{
      font-size: 14px;
      font-weight: 600;
      color: {theme.accent};
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 16px;
    }}
    .ask-amount {{
      font-family: {theme.headline_font_family};
      font-size: 72px;
      font-weight: 600;
      margin-bottom: 24px;
    }}
    .ask-uses {{
      font-size: 18px;
      color: {theme.text_secondary};
      line-height: 1.8;
    }}
    .contact {{
      font-size: 16px;
      color: {theme.text_muted};
      position: absolute;
      bottom: 60px;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="name">{founder_name}</div>
  <div class="title-text">{founder_title}</div>
  <div class="divider"></div>
  <div class="ask-section">
    <div class="ask-label">Investment Ask</div>
    <div class="ask-amount">{ask_amount}</div>
    <div class="ask-uses">{uses_html}</div>
  </div>
  <div class="contact">{contact_html}</div>
</body>
</html>'''

        # CONSUMER STYLE - Fun, gradient, playful
        elif 'consumer' in style:
            contact_lines = []
            if contact_info.get("email"):
                contact_lines.append(f"📧 {contact_info['email']}")
            if contact_info.get("linkedin"):
                contact_lines.append(f"🔗 {contact_info['linkedin']}")
            contact_html = "<br>".join(contact_lines) if contact_lines else ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Team & Ask</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .gradient-blob {{
      position: absolute;
      width: 700px;
      height: 700px;
      border-radius: 50%;
      background: {theme.gradient_primary};
      opacity: 0.15;
      filter: blur(100px);
      top: -200px;
      right: -100px;
    }}
    .content {{
      display: flex;
      gap: 80px;
      height: 100%;
      align-items: center;
    }}
    .left {{
      flex: 1;
    }}
    .name {{
      font-size: 56px;
      font-weight: 800;
      margin-bottom: 12px;
      background: {theme.gradient_text};
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .title-text {{
      font-size: 22px;
      color: {theme.text_secondary};
      margin-bottom: 40px;
    }}
    .bio-items {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .bio-item {{
      font-size: 18px;
      color: {theme.text_secondary};
    }}
    .bio-item .company {{
      color: {theme.accent};
      font-weight: 600;
    }}
    .right {{
      flex: 1;
    }}
    .ask-card {{
      background: {theme.gradient_primary};
      color: white;
      padding: 48px;
      border-radius: 32px;
      text-align: center;
    }}
    .ask-label {{
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      opacity: 0.8;
      margin-bottom: 16px;
    }}
    .ask-amount {{
      font-size: 72px;
      font-weight: 900;
      margin-bottom: 24px;
    }}
    .ask-uses {{
      font-size: 18px;
      line-height: 1.8;
      opacity: 0.9;
    }}
    .contact-box {{
      margin-top: 32px;
      padding: 28px;
      background: {theme.surface};
      border-radius: 20px;
      border: 2px solid {theme.border};
      font-size: 16px;
      color: {theme.text_secondary};
      line-height: 1.8;
    }}
  </style>
</head>
<body>
  <div class="gradient-blob"></div>
  <div class="content">
    <div class="left">
      <div class="name">{founder_name}</div>
      <div class="title-text">{founder_title}</div>
      <div class="bio-items">{bio_html}</div>
    </div>
    <div class="right">
      <div class="ask-card">
        <div class="ask-label">We're raising</div>
        <div class="ask-amount">{ask_amount}</div>
        <div class="ask-uses">{uses_html}</div>
      </div>
      <div class="contact-box">{contact_html}</div>
    </div>
  </div>
</body>
</html>'''

        # CREATIVE STYLE - Bold asymmetric
        elif 'creative' in style:
            contact_lines = []
            if contact_info.get("email"):
                contact_lines.append(contact_info["email"])
            if contact_info.get("linkedin"):
                contact_lines.append(contact_info["linkedin"])
            contact_html = "<br>".join(contact_lines) if contact_lines else ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Team & Ask</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .left {{
      flex: 1;
      background: {theme.accent};
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 80px;
      color: {theme.background};
    }}
    .name {{
      font-size: 64px;
      font-weight: 900;
      margin-bottom: 16px;
    }}
    .title-text {{
      font-size: 24px;
      opacity: 0.8;
      margin-bottom: 48px;
    }}
    .bio-items {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .bio-item {{
      font-size: 18px;
      opacity: 0.9;
    }}
    .bio-item .company {{
      font-weight: 700;
    }}
    .right {{
      flex: 1.2;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 80px;
    }}
    .ask-label {{
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: {theme.text_muted};
      margin-bottom: 24px;
    }}
    .ask-amount {{
      font-size: 96px;
      font-weight: 900;
      margin-bottom: 32px;
      line-height: 1;
    }}
    .ask-uses {{
      font-size: 20px;
      line-height: 1.8;
      color: {theme.text_secondary};
      margin-bottom: 48px;
    }}
    .contact-box {{
      padding-top: 32px;
      border-top: 2px solid {theme.border};
      font-size: 18px;
      color: {theme.text_muted};
      line-height: 1.8;
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="name">{founder_name}</div>
    <div class="title-text">{founder_title}</div>
    <div class="bio-items">{bio_html}</div>
  </div>
  <div class="right">
    <div class="ask-label">The Ask</div>
    <div class="ask-amount">{ask_amount}</div>
    <div class="ask-uses">{uses_html}</div>
    <div class="contact-box">{contact_html}</div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Clean, elegant
        elif 'minimal' in style:
            contact_lines = []
            if contact_info.get("email"):
                contact_lines.append(contact_info["email"])
            if contact_info.get("linkedin"):
                contact_lines.append(contact_info["linkedin"])
            contact_html = " · ".join(contact_lines) if contact_lines else ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Team & Ask</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
      display: flex;
      gap: 120px;
    }}
    .left {{
      flex: 1;
    }}
    .name {{
      font-size: 44px;
      font-weight: 400;
      margin-bottom: 12px;
      letter-spacing: -0.02em;
    }}
    .title-text {{
      font-size: 18px;
      font-weight: 300;
      color: {theme.text_secondary};
      margin-bottom: 60px;
    }}
    .bio-items {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .bio-item {{
      font-size: 16px;
      font-weight: 300;
      color: {theme.text_secondary};
    }}
    .bio-item .company {{
      font-weight: 500;
      color: {theme.text_primary};
    }}
    .right {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .ask-label {{
      font-size: 11px;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: {theme.text_muted};
      margin-bottom: 24px;
    }}
    .ask-amount {{
      font-size: 72px;
      font-weight: 300;
      margin-bottom: 32px;
      letter-spacing: -0.03em;
    }}
    .ask-uses {{
      font-size: 17px;
      font-weight: 300;
      line-height: 2;
      color: {theme.text_secondary};
    }}
    .contact {{
      position: absolute;
      bottom: 80px;
      font-size: 14px;
      color: {theme.text_muted};
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="name">{founder_name}</div>
    <div class="title-text">{founder_title}</div>
    <div class="bio-items">{bio_html}</div>
  </div>
  <div class="right">
    <div class="ask-label">Investment</div>
    <div class="ask-amount">{ask_amount}</div>
    <div class="ask-uses">{uses_html}</div>
  </div>
  <div class="contact">{contact_html}</div>
</body>
</html>'''

        # SALES STYLE - High contrast, CTA focused
        elif 'sales' in style:
            contact_lines = []
            if contact_info.get("email"):
                contact_lines.append(contact_info["email"])
            if contact_info.get("linkedin"):
                contact_lines.append(contact_info["linkedin"])
            contact_html = "<br>".join(contact_lines) if contact_lines else ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Team & Ask</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .left {{
      flex: 1;
      padding: 80px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .name {{
      font-size: 52px;
      font-weight: 800;
      margin-bottom: 12px;
    }}
    .title-text {{
      font-size: 22px;
      color: {theme.text_secondary};
      margin-bottom: 40px;
    }}
    .bio-items {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .bio-item {{
      font-size: 18px;
      color: {theme.text_secondary};
      display: flex;
      gap: 12px;
    }}
    .bio-item .company {{
      font-weight: 600;
      color: {theme.text_primary};
    }}
    .right {{
      flex: 1;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 80px;
    }}
    .ask-label {{
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: {theme.accent};
      margin-bottom: 20px;
    }}
    .ask-amount {{
      font-size: 80px;
      font-weight: 800;
      margin-bottom: 32px;
    }}
    .ask-uses {{
      font-size: 18px;
      line-height: 1.8;
      opacity: 0.9;
      margin-bottom: 48px;
    }}
    .cta-button {{
      display: inline-block;
      background: {theme.accent};
      color: white;
      padding: 16px 40px;
      border-radius: 8px;
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 24px;
    }}
    .contact-info {{
      font-size: 16px;
      opacity: 0.7;
      line-height: 1.8;
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="name">{founder_name}</div>
    <div class="title-text">{founder_title}</div>
    <div class="bio-items">{bio_html}</div>
  </div>
  <div class="right">
    <div class="ask-label">Let's Partner</div>
    <div class="ask-amount">{ask_amount}</div>
    <div class="ask-uses">{uses_html}</div>
    <div class="cta-button">Schedule a Call →</div>
    <div class="contact-info">{contact_html}</div>
  </div>
</body>
</html>'''

        # DEFAULT/TECH STYLE - Original layout
        photo_html = ""
        if founder_photo:
            photo_html = f'<img src="{founder_photo}" alt="{founder_name}" class="founder-photo">'

        looking_html = ""
        if looking_for:
            looking_html = f'''
        <div class="looking-for">
          <div class="looking-title">{looking_for.get("title", "")}</div>
          <div class="looking-text">{looking_for.get("text", "")}</div>
        </div>'''

        contact_html = ""
        if contact_info:
            contact_lines = []
            if contact_info.get("email"):
                contact_lines.append(contact_info["email"])
            if contact_info.get("linkedin"):
                contact_lines.append(contact_info["linkedin"])
            if contact_lines:
                contact_html = f'''
        <div class="contact-box">
          <div class="contact-label">Let's talk</div>
          <div class="contact-info">{"<br>".join(contact_lines)}</div>
        </div>'''

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Team & Ask</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      padding: {theme.slide_padding};
    }}
    .left {{
      flex: 1.3;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-right: 100px;
    }}
    .right {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .founder-photo {{
      width: 180px;
      height: 180px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 32px;
      border: 4px solid {theme.border};
    }}
    .name {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      margin-bottom: 16px;
    }}
    .title {{
      font-size: {theme.font_size_large};
      color: {theme.text_secondary};
      margin-bottom: 48px;
    }}
    .bio-section {{
      margin-bottom: 32px;
    }}
    .bio-label {{
      font-size: {theme.font_size_label};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
    }}
    .bio-items {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .bio-item {{
      font-size: 20px;
      color: {theme.text_secondary};
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .bio-item .company {{
      color: {theme.text_primary};
      font-weight: {theme.font_weight_semibold};
    }}
    .bio-item .detail {{
      color: {theme.text_muted};
    }}
    .looking-for {{
      margin-top: 48px;
      padding: 32px;
      background: {theme.surface};
      border-radius: {theme.radius_medium};
      border: 1px solid {theme.border};
    }}
    .looking-title {{
      font-size: 18px;
      font-weight: {theme.font_weight_semibold};
      margin-bottom: 12px;
      color: {theme.text_secondary};
    }}
    .looking-text {{
      font-size: 20px;
      color: {theme.text_primary};
      line-height: {theme.line_height_normal};
    }}
    .ask-box {{
      background: #fff;
      color: #000;
      padding: 48px;
      border-radius: {theme.radius_large};
      margin-bottom: 32px;
    }}
    .ask-label {{
      font-size: {theme.font_size_label};
      color: #666;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 16px;
    }}
    .ask-amount {{
      font-size: {theme.font_size_display};
      font-weight: {theme.font_weight_extrabold};
      margin-bottom: 24px;
    }}
    .ask-use {{
      font-size: 18px;
      color: #333;
      line-height: 1.7;
    }}
    .ask-use strong {{
      color: #000;
    }}
    .contact-box {{
      padding: 32px;
      border: 1px solid {theme.border};
      border-radius: {theme.radius_medium};
    }}
    .contact-label {{
      font-size: {theme.font_size_label};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 16px;
    }}
    .contact-info {{
      font-size: 20px;
      color: {theme.text_primary};
      line-height: 1.8;
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="label">Founder</div>
    {photo_html}
    <div class="name">{founder_name}</div>
    <div class="title">{founder_title}</div>
    <div class="bio-section">
      <div class="bio-label">Track record</div>
      <div class="bio-items">
        {bio_html}
      </div>
    </div>
    {looking_html}
  </div>
  <div class="right">
    <div class="ask-box">
      <div class="ask-label">The Ask</div>
      <div class="ask-amount">{ask_amount}</div>
      <div class="ask-use">
        <strong>12 months runway</strong> to:
        <br><br>
        {uses_html}
      </div>
    </div>
    {contact_html}
  </div>
</body>
</html>'''

    @staticmethod
    def render_content_slide(
        headline: str,
        content_html: str,
        label: Optional[str] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """Simple content slide with style-specific layouts."""
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        # CONSULTING STYLE - Bordered, structured
        if 'consulting' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-border {{ height: 4px; background: {theme.accent}; margin-bottom: 60px; }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: {theme.accent};
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 20px;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 48px;
      font-weight: 600;
      line-height: 1.2;
      color: {theme.text_primary};
      margin-bottom: 50px;
      padding-bottom: 30px;
      border-bottom: 1px solid {theme.border};
    }}
    .content {{
      font-size: 20px;
      line-height: 1.8;
      color: {theme.text_secondary};
      columns: 2;
      column-gap: 60px;
    }}
    .content p {{ margin-bottom: 20px; }}
  </style>
</head>
<body>
  <div class="top-border"></div>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="content">{content_html}</div>
</body>
</html>'''

        # CONSUMER STYLE - Rounded, warm
        elif 'consumer' in style:
            label_html = f'<span class="label">{label}</span>' if label else ''
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 120px;
      position: relative;
    }}
    .accent-circle {{
      position: absolute;
      width: 400px;
      height: 400px;
      border-radius: 50%;
      background: {theme.accent};
      opacity: 0.08;
      top: -100px;
      right: -100px;
    }}
    .label {{
      display: inline-block;
      background: {theme.accent};
      color: white;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 20px;
      border-radius: 20px;
      margin-bottom: 30px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      line-height: 1.15;
      color: {theme.text_primary};
      margin-bottom: 40px;
      max-width: 900px;
    }}
    .content {{
      font-size: 22px;
      line-height: 1.8;
      color: {theme.text_secondary};
      max-width: 1000px;
      background: {theme.surface};
      padding: 40px;
      border-radius: 24px;
    }}
  </style>
</head>
<body>
  <div class="accent-circle"></div>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="content">{content_html}</div>
</body>
</html>'''

        # CREATIVE STYLE - Bold, accent bar
        elif 'creative' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: grid;
      grid-template-columns: 80px 1fr;
    }}
    .accent-bar {{
      background: {theme.accent};
    }}
    .main {{
      padding: 80px 100px;
    }}
    .label {{
      font-size: 14px;
      font-weight: 700;
      color: {theme.accent};
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 24px;
    }}
    .headline {{
      font-size: 64px;
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -0.03em;
      margin-bottom: 50px;
      max-width: 1000px;
    }}
    .content {{
      font-size: 22px;
      line-height: 1.8;
      color: {theme.text_secondary};
      max-width: 1100px;
      padding-left: 30px;
      border-left: 4px solid {theme.accent};
    }}
  </style>
</head>
<body>
  <div class="accent-bar"></div>
  <div class="main">
    {label_html}
    <h1 class="headline">{headline}</h1>
    <div class="content">{content_html}</div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Sparse, elegant
        elif 'minimal' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .label {{
      font-size: 11px;
      font-weight: 500;
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.2em;
      margin-bottom: 40px;
    }}
    .headline {{
      font-size: 44px;
      font-weight: 300;
      line-height: 1.3;
      color: {theme.text_primary};
      margin-bottom: 50px;
      max-width: 800px;
    }}
    .content {{
      font-size: 19px;
      line-height: 2;
      color: {theme.text_secondary};
      max-width: 700px;
    }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="content">{content_html}</div>
</body>
</html>'''

        # SALES STYLE - Action-oriented
        elif 'sales' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 120px;
    }}
    .label {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 600;
      color: {theme.accent};
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 28px;
    }}
    .label::before {{
      content: '';
      width: 8px;
      height: 8px;
      background: {theme.accent};
      border-radius: 50%;
    }}
    .headline {{
      font-size: 54px;
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 40px;
      max-width: 1000px;
    }}
    .content {{
      font-size: 22px;
      line-height: 1.8;
      color: {theme.text_secondary};
      max-width: 1100px;
      background: {theme.surface};
      padding: 48px;
      border-radius: 16px;
      border-left: 6px solid {theme.accent};
    }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="content">{content_html}</div>
</body>
</html>'''

        # DEFAULT/TECH STYLE
        else:
            label_html = ""
            if label:
                label_html = f'<div class="label">{label}</div>'

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 48px;
    }}
    .content {{
      font-size: 24px;
      line-height: 1.7;
      color: {theme.text_secondary};
      max-width: 1400px;
    }}
    .content strong {{
      color: {theme.text_primary};
    }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="content">{content_html}</div>
</body>
</html>'''

    @staticmethod
    def render_two_column_slide(
        headline: str,
        left_content: str,
        right_content: str,
        label: Optional[str] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """Two-column layout slide with style-specific designs."""
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        label_html = ""
        if label:
            label_html = f'<div class="label">{label}</div>'

        # CONSULTING STYLE - Serif fonts, navy accents, structured boxes
        if 'consulting' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: 80px 100px;
    }}
    .top-bar {{
      height: 6px;
      background: #1a2744;
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: #1a2744;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 24px;
      padding-left: 16px;
      border-left: 3px solid #1a2744;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 52px;
      font-weight: 600;
      line-height: 1.15;
      color: #1a2744;
      margin-bottom: 60px;
    }}
    .columns {{
      display: flex;
      gap: 60px;
      flex: 1;
    }}
    .column {{
      flex: 1;
      background: #f8f9fb;
      padding: 40px;
      border-radius: 4px;
      border-top: 3px solid #1a2744;
    }}
    .column-content {{
      font-size: 20px;
      line-height: 1.8;
      color: #3d5a80;
    }}
    .column-content strong {{
      color: #1a2744;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="columns">
    <div class="column"><div class="column-content">{left_content}</div></div>
    <div class="column"><div class="column-content">{right_content}</div></div>
  </div>
</body>
</html>'''

        # CONSUMER STYLE - Pink gradients, rounded cards, playful
        elif 'consumer' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: linear-gradient(180deg, #fffbfc 0%, #fdf2f8 100%);
      color: #1f1f1f;
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .blob {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.4;
    }}
    .blob-1 {{ width: 400px; height: 400px; background: #ec4899; top: -100px; right: -100px; }}
    .blob-2 {{ width: 300px; height: 300px; background: #a855f7; bottom: -50px; left: -50px; }}
    .content {{ position: relative; z-index: 1; flex: 1; display: flex; flex-direction: column; }}
    .label {{
      display: inline-block;
      font-size: 13px;
      font-weight: 700;
      color: #ec4899;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 24px;
      background: rgba(236,72,153,0.1);
      padding: 8px 16px;
      border-radius: 20px;
    }}
    .headline {{
      font-size: 54px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 60px;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .columns {{
      display: flex;
      gap: 40px;
      flex: 1;
    }}
    .column {{
      flex: 1;
      background: white;
      padding: 48px;
      border-radius: 32px;
      box-shadow: 0 8px 32px rgba(236,72,153,0.12);
      border: 2px solid rgba(236,72,153,0.1);
    }}
    .column-content {{
      font-size: 20px;
      line-height: 1.8;
      color: #4a4a4a;
    }}
    .column-content strong {{
      color: #ec4899;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="content">
    {label_html}
    <h1 class="headline">{headline}</h1>
    <div class="columns">
      <div class="column"><div class="column-content">{left_content}</div></div>
      <div class="column"><div class="column-content">{right_content}</div></div>
    </div>
  </div>
</body>
</html>'''

        # CREATIVE STYLE - Bold typography, yellow accents, asymmetric
        elif 'creative' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0f0f0f;
      color: #ffffff;
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .sidebar {{
      width: 120px;
      background: #facc15;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: #0f0f0f;
    }}
    .main {{
      flex: 1;
      padding: 80px;
      display: flex;
      flex-direction: column;
    }}
    .headline {{
      font-size: 64px;
      font-weight: 900;
      line-height: 1.0;
      margin-bottom: 60px;
      text-transform: uppercase;
      letter-spacing: -0.03em;
    }}
    .headline span {{
      color: #facc15;
    }}
    .columns {{
      display: flex;
      gap: 60px;
      flex: 1;
    }}
    .column {{
      flex: 1;
      padding: 40px;
      border-left: 4px solid #facc15;
    }}
    .column-content {{
      font-size: 20px;
      line-height: 1.8;
      color: rgba(255,255,255,0.8);
    }}
    .column-content strong {{
      color: #facc15;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <div class="sidebar">
    <span class="sidebar-text">{label if label else 'COMPARE'}</span>
  </div>
  <div class="main">
    <h1 class="headline">{headline.replace('.', '.<span>*</span>')}</h1>
    <div class="columns">
      <div class="column"><div class="column-content">{left_content}</div></div>
      <div class="column"><div class="column-content">{right_content}</div></div>
    </div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Maximum whitespace, light typography
        elif 'minimal' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #fafafa;
      color: #171717;
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: 120px 160px;
    }}
    .label {{
      font-size: 11px;
      font-weight: 500;
      color: #a3a3a3;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 48px;
      font-weight: 500;
      line-height: 1.2;
      color: #171717;
      margin-bottom: 80px;
      letter-spacing: -0.02em;
    }}
    .columns {{
      display: flex;
      gap: 120px;
      flex: 1;
    }}
    .column {{
      flex: 1;
      padding-top: 24px;
      border-top: 1px solid #e5e5e5;
    }}
    .column-content {{
      font-size: 18px;
      line-height: 2;
      color: #525252;
      font-weight: 400;
    }}
    .column-content strong {{
      color: #171717;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="columns">
    <div class="column"><div class="column-content">{left_content}</div></div>
    <div class="column"><div class="column-content">{right_content}</div></div>
  </div>
</body>
</html>'''

        # SALES STYLE - Dark background, emerald accents, compelling
        elif 'sales' in style:
            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: linear-gradient(180deg, #0c1929 0%, #132337 100%);
      color: #ffffff;
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: 80px 100px;
    }}
    .label {{
      display: inline-block;
      font-size: 12px;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 24px;
      padding: 8px 16px;
      background: rgba(16,185,129,0.15);
      border-radius: 4px;
    }}
    .headline {{
      font-size: 56px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 60px;
    }}
    .headline-accent {{
      color: #10b981;
    }}
    .columns {{
      display: flex;
      gap: 48px;
      flex: 1;
    }}
    .column {{
      flex: 1;
      background: rgba(255,255,255,0.05);
      padding: 48px;
      border-radius: 16px;
      border: 1px solid rgba(16,185,129,0.2);
    }}
    .column-content {{
      font-size: 20px;
      line-height: 1.8;
      color: rgba(255,255,255,0.85);
    }}
    .column-content strong {{
      color: #10b981;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="columns">
    <div class="column"><div class="column-content">{left_content}</div></div>
    <div class="column"><div class="column-content">{right_content}</div></div>
  </div>
</body>
</html>'''

        # DEFAULT/TECH STYLE
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 60px;
    }}
    .columns {{
      display: flex;
      gap: 80px;
      flex: 1;
    }}
    .column {{
      flex: 1;
      font-size: 22px;
      line-height: 1.7;
      color: {theme.text_secondary};
    }}
    .column strong {{
      color: {theme.text_primary};
    }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="columns">
    <div class="column">{left_content}</div>
    <div class="column">{right_content}</div>
  </div>
</body>
</html>'''

    @staticmethod
    def render_quote_slide(
        quote: str,
        author: str,
        author_role: Optional[str] = None,
        author_avatar: Optional[str] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """Single large quote slide."""
        theme = theme or LightTheme()

        def get_initials(name: str) -> str:
            parts = name.split()
            return parts[0][0].upper() if parts else "?"

        avatar_html = ""
        if author_avatar:
            avatar_html = f'<img src="{author_avatar}" alt="{author}" class="avatar-img">'
        else:
            avatar_html = f'<div class="avatar">{get_initials(author)}</div>'

        role_html = ""
        if author_role:
            role_html = f'<div class="author-role">{author_role}</div>'

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Quote</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 120px;
    }}
    .quote {{
      font-size: 48px;
      font-weight: {theme.font_weight_medium};
      line-height: 1.4;
      text-align: center;
      max-width: 1400px;
      margin-bottom: 60px;
      color: {theme.text_primary};
    }}
    .quote::before {{
      content: """;
      font-size: 120px;
      color: {theme.accent};
      display: block;
      margin-bottom: 20px;
      line-height: 0.5;
    }}
    .author-section {{
      display: flex;
      align-items: center;
      gap: 20px;
    }}
    .avatar {{
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: {theme.surface};
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: {theme.font_weight_bold};
      font-size: 24px;
      color: {theme.text_muted};
    }}
    .avatar-img {{
      width: 64px;
      height: 64px;
      border-radius: 50%;
      object-fit: cover;
    }}
    .author-info {{
      text-align: left;
    }}
    .author-name {{
      font-size: 20px;
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_primary};
    }}
    .author-role {{
      font-size: 16px;
      color: {theme.text_muted};
      margin-top: 4px;
    }}
  </style>
</head>
<body>
  <div class="quote">{quote}</div>
  <div class="author-section">
    {avatar_html}
    <div class="author-info">
      <div class="author-name">{author}</div>
      {role_html}
    </div>
  </div>
</body>
</html>'''

    @staticmethod
    def render_numbered_points_slide(
        headline: str,
        points: List[Dict[str, str]],
        label: Optional[str] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """Numbered points slide with style-specific layouts."""
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        # CONSULTING STYLE - Horizontal cards with numbers
        if 'consulting' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            points_html = "\n".join(f'''
            <div class="point">
              <div class="point-num">{i + 1}</div>
              <div class="point-title">{point.get("title", "")}</div>
              <div class="point-desc">{point.get("description", "")}</div>
            </div>''' for i, point in enumerate(points))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-border {{ height: 4px; background: {theme.accent}; margin-bottom: 50px; }}
    .label {{ font-size: 12px; font-weight: 600; color: {theme.accent}; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 20px; }}
    .headline {{ font-family: {theme.headline_font_family}; font-size: 44px; font-weight: 600; margin-bottom: 50px; padding-bottom: 25px; border-bottom: 1px solid {theme.border}; }}
    .points {{ display: flex; gap: 40px; }}
    .point {{ flex: 1; background: {theme.surface}; padding: 40px; border-top: 4px solid {theme.accent}; }}
    .point-num {{ font-size: 48px; font-weight: 600; color: {theme.accent}; margin-bottom: 20px; }}
    .point-title {{ font-size: 20px; font-weight: 600; margin-bottom: 16px; color: {theme.text_primary}; }}
    .point-desc {{ font-size: 16px; color: {theme.text_secondary}; line-height: 1.6; }}
  </style>
</head>
<body>
  <div class="top-border"></div>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="points">{points_html}</div>
</body>
</html>'''

        # CONSUMER STYLE - Rounded cards
        elif 'consumer' in style:
            label_html = f'<span class="label">{label}</span>' if label else ''
            points_html = "\n".join(f'''
            <div class="point">
              <div class="point-icon">{i + 1}</div>
              <div class="point-title">{point.get("title", "")}</div>
              <div class="point-desc">{point.get("description", "")}</div>
            </div>''' for i, point in enumerate(points))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; padding: 80px 100px; }}
    .label {{ display: inline-block; background: {theme.accent}; color: white; font-size: 13px; font-weight: 600; padding: 8px 20px; border-radius: 20px; margin-bottom: 30px; }}
    .headline {{ font-size: 48px; font-weight: 800; margin-bottom: 50px; max-width: 900px; }}
    .points {{ display: flex; gap: 32px; }}
    .point {{ flex: 1; background: {theme.surface}; padding: 40px; border-radius: 24px; }}
    .point-icon {{ width: 56px; height: 56px; background: {theme.gradient_primary}; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; color: white; margin-bottom: 24px; }}
    .point-title {{ font-size: 22px; font-weight: 700; margin-bottom: 12px; }}
    .point-desc {{ font-size: 17px; color: {theme.text_secondary}; line-height: 1.6; }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="points">{points_html}</div>
</body>
</html>'''

        # CREATIVE STYLE - Large numbers
        elif 'creative' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            points_html = "\n".join(f'''
            <div class="point">
              <div class="point-num">{i + 1}</div>
              <div class="point-text">
                <div class="point-title">{point.get("title", "")}</div>
                <div class="point-desc">{point.get("description", "")}</div>
              </div>
            </div>''' for i, point in enumerate(points))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; display: grid; grid-template-columns: 80px 1fr; }}
    .accent-bar {{ background: {theme.accent}; }}
    .main {{ padding: 80px 100px; }}
    .label {{ font-size: 14px; font-weight: 700; color: {theme.accent}; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 24px; }}
    .headline {{ font-size: 56px; font-weight: 900; line-height: 1.05; letter-spacing: -0.03em; margin-bottom: 60px; }}
    .points {{ display: flex; flex-direction: column; gap: 40px; }}
    .point {{ display: flex; align-items: flex-start; gap: 40px; }}
    .point-num {{ font-size: 72px; font-weight: 900; color: {theme.accent}; line-height: 1; min-width: 80px; }}
    .point-title {{ font-size: 26px; font-weight: 700; margin-bottom: 8px; }}
    .point-desc {{ font-size: 18px; color: {theme.text_secondary}; line-height: 1.5; }}
  </style>
</head>
<body>
  <div class="accent-bar"></div>
  <div class="main">
    {label_html}
    <h1 class="headline">{headline}</h1>
    <div class="points">{points_html}</div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Simple, clean
        elif 'minimal' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            points_html = "\n".join(f'''
            <div class="point">
              <div class="point-num">{i + 1}.</div>
              <div class="point-text">
                <span class="point-title">{point.get("title", "")}</span>
                <span class="point-desc">— {point.get("description", "")}</span>
              </div>
            </div>''' for i, point in enumerate(points))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; padding: 120px 160px; display: flex; flex-direction: column; justify-content: center; }}
    .label {{ font-size: 11px; font-weight: 500; color: {theme.text_muted}; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 40px; }}
    .headline {{ font-size: 40px; font-weight: 300; margin-bottom: 60px; max-width: 700px; }}
    .points {{ display: flex; flex-direction: column; gap: 32px; max-width: 900px; }}
    .point {{ display: flex; gap: 20px; font-size: 20px; line-height: 1.6; }}
    .point-num {{ color: {theme.text_muted}; min-width: 30px; }}
    .point-title {{ font-weight: 500; }}
    .point-desc {{ color: {theme.text_secondary}; }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="points">{points_html}</div>
</body>
</html>'''

        # SALES STYLE - Check marks
        elif 'sales' in style:
            label_html = f'<div class="label">{label}</div>' if label else ''
            points_html = "\n".join(f'''
            <div class="point">
              <div class="point-check">✓</div>
              <div class="point-content">
                <div class="point-title">{point.get("title", "")}</div>
                <div class="point-desc">{point.get("description", "")}</div>
              </div>
            </div>''' for i, point in enumerate(points))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; padding: 80px 120px; }}
    .label {{ display: inline-flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: {theme.accent}; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 28px; }}
    .label::before {{ content: ''; width: 8px; height: 8px; background: {theme.accent}; border-radius: 50%; }}
    .headline {{ font-size: 50px; font-weight: 800; margin-bottom: 50px; max-width: 900px; }}
    .points {{ display: flex; flex-direction: column; gap: 32px; }}
    .point {{ display: flex; align-items: flex-start; gap: 24px; background: {theme.surface}; padding: 32px; border-radius: 16px; }}
    .point-check {{ width: 40px; height: 40px; background: {theme.accent}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }}
    .point-title {{ font-size: 22px; font-weight: 700; margin-bottom: 8px; }}
    .point-desc {{ font-size: 18px; color: {theme.text_secondary}; line-height: 1.5; }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="points">{points_html}</div>
</body>
</html>'''

        # DEFAULT/TECH STYLE
        else:
            label_html = ""
            if label:
                label_html = f'<div class="label">{label}</div>'

            points_html = "\n".join(f'''
            <div class="point">
              <div class="point-number">{i + 1}</div>
              <div class="point-content">
                <div class="point-title">{point.get("title", "")}</div>
                <div class="point-desc">{point.get("description", "")}</div>
              </div>
            </div>''' for i, point in enumerate(points))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: {theme.slide_padding};
    }}
    .label {{ font-size: {theme.font_size_label}; font-weight: {theme.font_weight_semibold}; color: {theme.text_muted}; text-transform: uppercase; letter-spacing: {theme.letter_spacing_wide}; margin-bottom: 32px; }}
    .headline {{ font-size: {theme.font_size_headline}; font-weight: {theme.font_weight_extrabold}; line-height: {theme.line_height_tight}; letter-spacing: {theme.letter_spacing_tight}; margin-bottom: 60px; }}
    .points {{ display: flex; flex-direction: column; gap: 40px; }}
    .point {{ display: flex; align-items: flex-start; gap: 32px; }}
    .point-number {{ width: 48px; height: 48px; border-radius: 50%; border: 2px solid {theme.border}; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: {theme.font_weight_bold}; color: {theme.text_secondary}; flex-shrink: 0; }}
    .point-content {{ flex: 1; }}
    .point-title {{ font-size: 28px; font-weight: {theme.font_weight_bold}; margin-bottom: 12px; color: {theme.text_primary}; }}
    .point-desc {{ font-size: 20px; color: {theme.text_muted}; line-height: 1.5; }}
  </style>
</head>
<body>
  {label_html}
  <h1 class="headline">{headline}</h1>
  <div class="points">
    {points_html}
  </div>
</body>
</html>'''

    @staticmethod
    def render_comparison_slide(
        headline: str,
        columns: List[Dict[str, Any]],
        highlight_column: int = -1,
        label: Optional[str] = "Comparison",
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render competitive comparison matrix with style-specific layouts.
        columns: List of {name, subtitle?, items: List[{text, good: bool}], bottom_line?}
        """
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        # =====================================================================
        # CONSULTING STYLE - Professional table matrix with structured rows
        # =====================================================================
        if 'consulting' in style:
            # Build table rows from items
            max_items = max(len(col.get("items", [])) for col in columns) if columns else 0

            header_cells = "".join(f'''
                <th class="{"highlight" if i == highlight_column else ""}">{col.get("name", "")}</th>
            ''' for i, col in enumerate(columns))

            rows_html = ""
            for row_idx in range(max_items):
                cells = ""
                for col_idx, col in enumerate(columns):
                    items = col.get("items", [])
                    if row_idx < len(items):
                        item = items[row_idx]
                        is_good = item.get('good', False)
                        icon = "✓" if is_good else "—"
                        cells += f'''<td class="{"highlight" if col_idx == highlight_column else ""} {"good" if is_good else "bad"}">{icon} {item.get('text', '')}</td>'''
                    else:
                        cells += f'''<td class="{"highlight" if col_idx == highlight_column else ""}"></td>'''
                rows_html += f"<tr>{cells}</tr>"

            verdict_cells = "".join(f'''
                <td class="verdict {"highlight" if i == highlight_column else ""}">{col.get("bottom_line", "")}</td>
            ''' for i, col in enumerate(columns))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Source Sans Pro', sans-serif;
      background: #ffffff;
      color: #1a2744;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-bar {{
      width: 100%;
      height: 8px;
      background: #1a2744;
      position: absolute;
      top: 0;
      left: 0;
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: #4a90d9;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 48px;
      font-weight: 700;
      color: #1a2744;
      margin-bottom: 50px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 18px;
    }}
    th {{
      background: #f5f7fa;
      padding: 24px 20px;
      text-align: left;
      font-weight: 600;
      font-size: 20px;
      border-bottom: 2px solid #1a2744;
    }}
    th.highlight {{
      background: #1a2744;
      color: #ffffff;
    }}
    td {{
      padding: 20px;
      border-bottom: 1px solid #e8ecf2;
      vertical-align: top;
    }}
    td.highlight {{
      background: rgba(26, 39, 68, 0.03);
    }}
    td.good {{
      color: #1a2744;
      font-weight: 600;
    }}
    td.bad {{
      color: #8896a8;
    }}
    .verdict {{
      font-weight: 600;
      padding-top: 24px;
      border-top: 2px solid #1a2744;
      border-bottom: none;
      font-size: 16px;
      color: #4a90d9;
    }}
    .verdict.highlight {{
      color: #1a2744;
      font-size: 18px;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <table>
    <thead><tr>{header_cells}</tr></thead>
    <tbody>{rows_html}</tbody>
    <tfoot><tr>{verdict_cells}</tr></tfoot>
  </table>
</body>
</html>'''

        # =====================================================================
        # CONSUMER STYLE - Colorful cards with friendly icons
        # =====================================================================
        elif 'consumer' in style:
            def render_consumer_column(col: Dict, idx: int) -> str:
                is_highlighted = idx == highlight_column

                items_html = "".join(f'''
                    <div class="item {'good' if item.get('good', False) else 'bad'}">
                        <span class="icon">{'💚' if item.get('good', False) else '💔'}</span>
                        <span>{item.get('text', '')}</span>
                    </div>
                ''' for item in col.get("items", []))

                bottom_html = f'<div class="bottom-line">{col.get("bottom_line", "")}</div>' if col.get("bottom_line") else ""
                subtitle_html = f'<div class="subtitle">{col.get("subtitle", "")}</div>' if col.get("subtitle") else ""

                return f'''
                <div class="card {"highlight" if is_highlighted else ""}">
                    <div class="card-header">
                        <div class="name">{col.get("name", "")}</div>
                        {subtitle_html}
                    </div>
                    <div class="items">{items_html}</div>
                    {bottom_html}
                </div>'''

            columns_html = "".join(render_consumer_column(col, i) for i, col in enumerate(columns))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: linear-gradient(180deg, #fffbfc 0%, #fdf2f8 100%);
      color: #1f1f1f;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .blob {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.4;
    }}
    .blob-1 {{ width: 400px; height: 400px; background: #ec4899; top: -100px; right: 200px; }}
    .blob-2 {{ width: 300px; height: 300px; background: #a855f7; bottom: 100px; left: -50px; }}
    .content {{ position: relative; z-index: 1; }}
    .label {{
      display: inline-block;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      color: white;
      font-size: 13px;
      font-weight: 700;
      padding: 8px 20px;
      border-radius: 50px;
      margin-bottom: 24px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      color: #1f1f1f;
      margin-bottom: 50px;
    }}
    .cards {{
      display: flex;
      gap: 28px;
    }}
    .card {{
      flex: 1;
      background: white;
      border-radius: 24px;
      padding: 32px;
      box-shadow: 0 4px 24px rgba(236, 72, 153, 0.1);
    }}
    .card.highlight {{
      background: linear-gradient(135deg, #ec4899, #db2777);
      color: white;
      transform: scale(1.02);
    }}
    .card-header {{
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 2px solid #fce7f3;
    }}
    .card.highlight .card-header {{
      border-bottom-color: rgba(255,255,255,0.2);
    }}
    .name {{
      font-size: 24px;
      font-weight: 700;
    }}
    .subtitle {{
      font-size: 14px;
      opacity: 0.6;
      margin-top: 6px;
    }}
    .items {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .item {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 17px;
    }}
    .item.good {{
      font-weight: 600;
    }}
    .item.bad {{
      opacity: 0.5;
    }}
    .icon {{
      font-size: 18px;
    }}
    .bottom-line {{
      margin-top: 24px;
      padding-top: 20px;
      border-top: 2px solid #fce7f3;
      font-weight: 700;
      font-size: 16px;
      color: #ec4899;
    }}
    .card.highlight .bottom-line {{
      border-top-color: rgba(255,255,255,0.2);
      color: white;
    }}
  </style>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="content">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="cards">{columns_html}</div>
  </div>
</body>
</html>'''

        # =====================================================================
        # CREATIVE STYLE - Bold asymmetric with accent sidebar
        # =====================================================================
        elif 'creative' in style:
            def render_creative_column(col: Dict, idx: int) -> str:
                is_highlighted = idx == highlight_column

                items_html = "".join(f'''
                    <div class="item {'good' if item.get('good', False) else 'bad'}">
                        <span class="mark">{'✓' if item.get('good', False) else '✗'}</span>
                        {item.get('text', '')}
                    </div>
                ''' for item in col.get("items", []))

                bottom_html = f'<div class="verdict">{col.get("bottom_line", "")}</div>' if col.get("bottom_line") else ""

                return f'''
                <div class="column {"winner" if is_highlighted else ""}">
                    <div class="col-header">
                        <div class="col-name">{col.get("name", "")}</div>
                        {"<span class='badge'>WINNER</span>" if is_highlighted else ""}
                    </div>
                    <div class="items">{items_html}</div>
                    {bottom_html}
                </div>'''

            columns_html = "".join(render_creative_column(col, i) for i, col in enumerate(columns))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0f0f0f;
      color: #f5f5f5;
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .sidebar {{
      width: 100px;
      background: #facc15;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 4px;
      color: #0f0f0f;
    }}
    .main {{
      flex: 1;
      padding: 80px;
    }}
    .label {{
      font-size: 13px;
      font-weight: 800;
      color: #facc15;
      text-transform: uppercase;
      letter-spacing: 3px;
      margin-bottom: 24px;
    }}
    .headline {{
      font-size: 60px;
      font-weight: 900;
      line-height: 1.0;
      margin-bottom: 60px;
      max-width: 900px;
    }}
    .columns {{
      display: flex;
      gap: 32px;
    }}
    .column {{
      flex: 1;
      background: #1a1a1a;
      padding: 32px;
      border-radius: 0;
    }}
    .column.winner {{
      background: #facc15;
      color: #0f0f0f;
    }}
    .col-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 3px solid rgba(255,255,255,0.1);
    }}
    .column.winner .col-header {{
      border-bottom-color: rgba(0,0,0,0.2);
    }}
    .col-name {{
      font-size: 22px;
      font-weight: 800;
      text-transform: uppercase;
    }}
    .badge {{
      font-size: 11px;
      font-weight: 800;
      background: #0f0f0f;
      color: #facc15;
      padding: 6px 14px;
    }}
    .items {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .item {{
      font-size: 17px;
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .item.good {{
      font-weight: 600;
    }}
    .item.bad {{
      opacity: 0.4;
    }}
    .mark {{
      font-weight: 800;
      font-size: 16px;
    }}
    .item.good .mark {{
      color: #22c55e;
    }}
    .item.bad .mark {{
      color: #ef4444;
    }}
    .column.winner .item.good .mark,
    .column.winner .item.bad .mark {{
      color: #0f0f0f;
    }}
    .verdict {{
      margin-top: 28px;
      padding-top: 20px;
      border-top: 3px solid rgba(255,255,255,0.1);
      font-weight: 800;
      font-size: 15px;
      text-transform: uppercase;
    }}
    .column.winner .verdict {{
      border-top-color: rgba(0,0,0,0.2);
    }}
  </style>
</head>
<body>
  <div class="sidebar"><span class="sidebar-text">Comparison Matrix</span></div>
  <div class="main">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="columns">{columns_html}</div>
  </div>
</body>
</html>'''

        # =====================================================================
        # MINIMAL STYLE - Clean whitespace, subtle borders
        # =====================================================================
        elif 'minimal' in style:
            def render_minimal_column(col: Dict, idx: int) -> str:
                is_highlighted = idx == highlight_column

                items_html = "".join(f'''
                    <div class="item {'good' if item.get('good', False) else 'bad'}">
                        {item.get('text', '')}
                    </div>
                ''' for item in col.get("items", []))

                bottom_html = f'<div class="summary">{col.get("bottom_line", "")}</div>' if col.get("bottom_line") else ""

                return f'''
                <div class="column {"active" if is_highlighted else ""}">
                    <div class="name">{col.get("name", "")}</div>
                    <div class="items">{items_html}</div>
                    {bottom_html}
                </div>'''

            columns_html = "".join(render_minimal_column(col, i) for i, col in enumerate(columns))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #fafafa;
      color: #171717;
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
    }}
    .label {{
      font-size: 12px;
      font-weight: 500;
      color: #a3a3a3;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 44px;
      font-weight: 300;
      letter-spacing: -0.02em;
      margin-bottom: 80px;
      color: #171717;
    }}
    .columns {{
      display: flex;
      gap: 1px;
      background: #e5e5e5;
    }}
    .column {{
      flex: 1;
      background: #fafafa;
      padding: 48px 40px;
    }}
    .column.active {{
      background: #171717;
      color: #fafafa;
    }}
    .name {{
      font-size: 18px;
      font-weight: 500;
      margin-bottom: 40px;
      padding-bottom: 20px;
      border-bottom: 1px solid #e5e5e5;
    }}
    .column.active .name {{
      border-bottom-color: #404040;
    }}
    .items {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .item {{
      font-size: 16px;
      font-weight: 400;
      line-height: 1.5;
    }}
    .item.good {{
      color: #171717;
    }}
    .item.bad {{
      color: #a3a3a3;
      text-decoration: line-through;
      text-decoration-color: #d4d4d4;
    }}
    .column.active .item.good {{
      color: #fafafa;
    }}
    .column.active .item.bad {{
      color: #737373;
    }}
    .summary {{
      margin-top: 40px;
      padding-top: 24px;
      border-top: 1px solid #e5e5e5;
      font-size: 14px;
      font-weight: 500;
      color: #737373;
    }}
    .column.active .summary {{
      border-top-color: #404040;
      color: #a3a3a3;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="columns">{columns_html}</div>
</body>
</html>'''

        # =====================================================================
        # SALES STYLE - High contrast with clear winner, action-oriented
        # =====================================================================
        elif 'sales' in style:
            def render_sales_column(col: Dict, idx: int) -> str:
                is_highlighted = idx == highlight_column

                items_html = "".join(f'''
                    <div class="feature {'yes' if item.get('good', False) else 'no'}">
                        <span class="check">{'✓' if item.get('good', False) else '✗'}</span>
                        <span class="text">{item.get('text', '')}</span>
                    </div>
                ''' for item in col.get("items", []))

                bottom_html = f'<div class="tagline">{col.get("bottom_line", "")}</div>' if col.get("bottom_line") else ""
                subtitle_html = f'<div class="type">{col.get("subtitle", "")}</div>' if col.get("subtitle") else ""

                return f'''
                <div class="option {"recommended" if is_highlighted else ""}">
                    {"<div class='ribbon'>RECOMMENDED</div>" if is_highlighted else ""}
                    <div class="option-name">{col.get("name", "")}</div>
                    {subtitle_html}
                    <div class="features">{items_html}</div>
                    {bottom_html}
                </div>'''

            columns_html = "".join(render_sales_column(col, i) for i, col in enumerate(columns))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0c1929;
      color: #ffffff;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .label {{
      font-size: 13px;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      margin-bottom: 50px;
    }}
    .options {{
      display: flex;
      gap: 28px;
      align-items: stretch;
    }}
    .option {{
      flex: 1;
      background: #132337;
      border-radius: 16px;
      padding: 36px;
      position: relative;
      border: 2px solid transparent;
    }}
    .option.recommended {{
      background: linear-gradient(180deg, #132337 0%, #1a3a4f 100%);
      border-color: #10b981;
      transform: scale(1.02);
    }}
    .ribbon {{
      position: absolute;
      top: -1px;
      left: 50%;
      transform: translateX(-50%);
      background: #10b981;
      color: #0c1929;
      font-size: 11px;
      font-weight: 700;
      padding: 6px 20px;
      border-radius: 0 0 8px 8px;
    }}
    .option-name {{
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 8px;
      margin-top: 16px;
    }}
    .type {{
      font-size: 14px;
      color: rgba(255,255,255,0.5);
      margin-bottom: 28px;
    }}
    .features {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .feature {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 16px;
    }}
    .feature.yes {{
      color: #ffffff;
    }}
    .feature.no {{
      color: rgba(255,255,255,0.4);
    }}
    .check {{
      width: 24px;
      height: 24px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 700;
    }}
    .feature.yes .check {{
      background: rgba(16, 185, 129, 0.2);
      color: #10b981;
    }}
    .feature.no .check {{
      background: rgba(239, 68, 68, 0.2);
      color: #ef4444;
    }}
    .tagline {{
      margin-top: 28px;
      padding-top: 20px;
      border-top: 1px solid rgba(255,255,255,0.1);
      font-size: 15px;
      font-weight: 600;
      color: rgba(255,255,255,0.7);
    }}
    .option.recommended .tagline {{
      color: #10b981;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="options">{columns_html}</div>
</body>
</html>'''

        # =====================================================================
        # DEFAULT/TECH STYLE - Modern tech aesthetic
        # =====================================================================
        def render_column(col: Dict, idx: int) -> str:
            is_highlighted = idx == highlight_column
            bg = "#000" if is_highlighted else theme.surface
            text_color = "#fff" if is_highlighted else theme.text_primary

            subtitle_html = ""
            if col.get("subtitle"):
                subtitle_html = f'<div class="col-subtitle">{col["subtitle"]}</div>'

            items_html = "\n".join(f'''
            <div class="col-item {'good' if item.get('good', False) else 'bad'}">
              <span class="indicator">{'●' if item.get('good', False) else '○'}</span>
              {item.get('text', '')}
            </div>''' for item in col.get("items", []))

            bottom_html = ""
            if col.get("bottom_line"):
                bottom_html = f'<div class="col-bottom">{col["bottom_line"]}</div>'

            return f'''
            <div class="column" style="background: {bg}; color: {text_color};">
              <div class="col-name">{col.get("name", "")}</div>
              {subtitle_html}
              <div class="col-items">{items_html}</div>
              {bottom_html}
            </div>'''

        columns_html = "\n".join(render_column(col, i) for i, col in enumerate(columns))

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 60px;
    }}
    .columns-grid {{
      display: flex;
      gap: 24px;
      flex: 1;
    }}
    .column {{
      flex: 1;
      padding: 32px;
      border-radius: {theme.radius_medium};
      display: flex;
      flex-direction: column;
    }}
    .col-name {{
      font-size: 24px;
      font-weight: {theme.font_weight_bold};
      margin-bottom: 8px;
    }}
    .col-subtitle {{
      font-size: 14px;
      opacity: 0.6;
      margin-bottom: 24px;
    }}
    .col-items {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      flex: 1;
    }}
    .col-item {{
      font-size: 18px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .col-item.good {{
      font-weight: {theme.font_weight_semibold};
    }}
    .col-item.bad {{
      opacity: 0.6;
    }}
    .indicator {{
      font-size: 12px;
    }}
    .col-bottom {{
      margin-top: 24px;
      padding-top: 24px;
      border-top: 1px solid rgba(128,128,128,0.2);
      font-size: 16px;
      font-weight: {theme.font_weight_semibold};
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="columns-grid">
    {columns_html}
  </div>
</body>
</html>'''

    @staticmethod
    def render_solution_slide(
        headline: str,
        subheadline: str,
        features: List[Dict[str, str]],
        label: Optional[str] = "Solution",
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render solution slide with style-specific feature layouts.
        features: List of {title, description}
        """
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        # CONSULTING STYLE - Numbered steps, structured framework
        if 'consulting' in style:
            features_html = "".join(f'''
            <div class="feature-row">
              <div class="feature-num">{i+1}</div>
              <div class="feature-content">
                <div class="feature-title">{f.get("title", "")}</div>
                <div class="feature-desc">{f.get("description", "")}</div>
              </div>
            </div>''' for i, f in enumerate(features[:4]))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-bar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: {theme.accent};
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: {theme.accent};
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 24px;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 48px;
      font-weight: 600;
      line-height: 1.2;
      margin-bottom: 20px;
    }}
    .subheadline {{
      font-size: 20px;
      color: {theme.text_secondary};
      margin-bottom: 60px;
      max-width: 800px;
      line-height: 1.6;
    }}
    .features-list {{
      display: flex;
      flex-direction: column;
      gap: 0;
    }}
    .feature-row {{
      display: flex;
      gap: 32px;
      padding: 32px 0;
      border-bottom: 1px solid {theme.border};
    }}
    .feature-row:last-child {{
      border-bottom: none;
    }}
    .feature-num {{
      width: 48px;
      height: 48px;
      background: {theme.accent};
      color: white;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 20px;
      flex-shrink: 0;
    }}
    .feature-content {{
      flex: 1;
    }}
    .feature-title {{
      font-size: 22px;
      font-weight: 600;
      margin-bottom: 8px;
    }}
    .feature-desc {{
      font-size: 17px;
      color: {theme.text_secondary};
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="features-list">
    {features_html}
  </div>
</body>
</html>'''

        # CONSUMER STYLE - Colorful cards with icons
        elif 'consumer' in style:
            icons = ["✨", "🎯", "⚡", "🚀"]
            features_html = "".join(f'''
            <div class="feature-card">
              <div class="feature-icon">{icons[i % len(icons)]}</div>
              <div class="feature-title">{f.get("title", "")}</div>
              <div class="feature-desc">{f.get("description", "")}</div>
            </div>''' for i, f in enumerate(features[:4]))

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .gradient-blob {{
      position: absolute;
      width: 700px;
      height: 700px;
      border-radius: 50%;
      background: {theme.gradient_primary};
      opacity: 0.12;
      filter: blur(100px);
      top: -200px;
      right: -100px;
    }}
    .label {{
      display: inline-block;
      background: {theme.accent};
      color: white;
      padding: 8px 20px;
      border-radius: 100px;
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 16px;
      background: {theme.gradient_text};
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subheadline {{
      font-size: 22px;
      color: {theme.text_secondary};
      margin-bottom: 50px;
      max-width: 700px;
    }}
    .features-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
    }}
    .feature-card {{
      background: {theme.surface};
      padding: 36px 28px;
      border-radius: 24px;
      border: 2px solid {theme.border};
      text-align: center;
    }}
    .feature-icon {{
      font-size: 48px;
      margin-bottom: 20px;
    }}
    .feature-title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 12px;
    }}
    .feature-desc {{
      font-size: 15px;
      line-height: 1.5;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="gradient-blob"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="features-grid">
    {features_html}
  </div>
</body>
</html>'''

        # CREATIVE STYLE - Bold asymmetric with sidebar
        elif 'creative' in style:
            features_html = "".join(f'''
            <div class="feature-block">
              <div class="feature-title">{f.get("title", "")}</div>
              <div class="feature-desc">{f.get("description", "")}</div>
            </div>''' for f in features[:4])

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: grid;
      grid-template-columns: 100px 1fr;
    }}
    .sidebar {{
      background: {theme.accent};
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: {theme.background};
    }}
    .main {{
      padding: 80px 100px;
    }}
    .headline {{
      font-size: 64px;
      font-weight: 900;
      line-height: 1.05;
      margin-bottom: 16px;
    }}
    .subheadline {{
      font-size: 22px;
      color: {theme.text_secondary};
      margin-bottom: 60px;
      max-width: 700px;
    }}
    .features-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 40px;
    }}
    .feature-block {{
      border-left: 4px solid {theme.accent};
      padding-left: 28px;
    }}
    .feature-title {{
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 12px;
    }}
    .feature-desc {{
      font-size: 17px;
      line-height: 1.6;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-text">{label}</div>
  </div>
  <div class="main">
    <h1 class="headline">{headline}</h1>
    <p class="subheadline">{subheadline}</p>
    <div class="features-grid">
      {features_html}
    </div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Clean, spacious
        elif 'minimal' in style:
            features_html = "".join(f'''
            <div class="feature-item">
              <div class="feature-title">{f.get("title", "")}</div>
              <div class="feature-desc">{f.get("description", "")}</div>
            </div>''' for f in features[:4])

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
    }}
    .label {{
      font-size: 11px;
      font-weight: 500;
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.2em;
      margin-bottom: 48px;
    }}
    .headline {{
      font-size: 44px;
      font-weight: 400;
      line-height: 1.3;
      margin-bottom: 16px;
      letter-spacing: -0.02em;
    }}
    .subheadline {{
      font-size: 18px;
      font-weight: 300;
      color: {theme.text_secondary};
      margin-bottom: 80px;
      max-width: 600px;
    }}
    .features-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 60px 100px;
    }}
    .feature-item {{
    }}
    .feature-title {{
      font-size: 20px;
      font-weight: 500;
      margin-bottom: 12px;
    }}
    .feature-desc {{
      font-size: 16px;
      font-weight: 300;
      line-height: 1.7;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="features-grid">
    {features_html}
  </div>
</body>
</html>'''

        # SALES STYLE - Action-oriented with check marks
        elif 'sales' in style:
            features_html = "".join(f'''
            <div class="feature-card">
              <div class="feature-check">✓</div>
              <div class="feature-content">
                <div class="feature-title">{f.get("title", "")}</div>
                <div class="feature-desc">{f.get("description", "")}</div>
              </div>
            </div>''' for f in features[:4])

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .label {{
      display: inline-block;
      background: #ecfdf5;
      color: #059669;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 16px;
    }}
    .subheadline {{
      font-size: 22px;
      color: {theme.text_secondary};
      margin-bottom: 60px;
      max-width: 800px;
    }}
    .features-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 32px;
    }}
    .feature-card {{
      display: flex;
      gap: 24px;
      background: {theme.surface};
      padding: 36px;
      border-radius: 16px;
      border: 1px solid {theme.border};
    }}
    .feature-check {{
      width: 40px;
      height: 40px;
      background: {theme.accent};
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 20px;
      flex-shrink: 0;
    }}
    .feature-content {{
      flex: 1;
    }}
    .feature-title {{
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .feature-desc {{
      font-size: 16px;
      line-height: 1.5;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="features-grid">
    {features_html}
  </div>
</body>
</html>'''

        # DEFAULT/TECH STYLE - Original 2x2 grid
        features_html = "\n".join(f'''
        <div class="feature-card">
          <div class="feature-title">{f.get("title", "")}</div>
          <div class="feature-desc">{f.get("description", "")}</div>
        </div>''' for f in features[:4])

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 20px;
    }}
    .subheadline {{
      font-size: {theme.font_size_large};
      color: {theme.text_secondary};
      margin-bottom: 60px;
      max-width: 900px;
      line-height: {theme.line_height_normal};
    }}
    .features-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 32px;
      flex: 1;
    }}
    .feature-card {{
      background: {theme.surface};
      padding: 40px;
      border-radius: {theme.radius_large};
    }}
    .feature-title {{
      font-size: 24px;
      font-weight: {theme.font_weight_bold};
      margin-bottom: 16px;
      color: {theme.text_primary};
    }}
    .feature-desc {{
      font-size: 18px;
      line-height: 1.6;
      color: {theme.text_secondary};
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="features-grid">
    {features_html}
  </div>
</body>
</html>'''

    @staticmethod
    def render_funds_slide(
        headline: str,
        subheadline: str,
        fund_items: List[Dict[str, Any]],
        milestones: List[Dict[str, str]],
        label: Optional[str] = "Use of Funds",
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render use of funds breakdown with style-specific layouts.
        fund_items: List of {label, amount, percentage}
        milestones: List of {month, text}
        """
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        # =====================================================================
        # CONSULTING STYLE - Professional allocation table
        # =====================================================================
        if 'consulting' in style:
            # Build allocation table rows
            table_rows = ""
            for item in fund_items:
                pct = item.get("percentage", 0)
                table_rows += f'''
                <tr>
                    <td class="alloc-category">{item.get("label", "")}</td>
                    <td class="alloc-amount">{item.get("amount", "")}</td>
                    <td class="alloc-pct">{pct}%</td>
                    <td class="alloc-bar-cell">
                        <div class="alloc-bar"><div class="alloc-fill" style="width: {pct}%;"></div></div>
                    </td>
                </tr>'''

            # Build milestone phases
            phases_html = ""
            for i, m in enumerate(milestones, 1):
                phases_html += f'''
                <div class="phase">
                    <div class="phase-num">{i}</div>
                    <div class="phase-info">
                        <div class="phase-time">{m.get("month", "")}</div>
                        <div class="phase-desc">{m.get("text", "")}</div>
                    </div>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Source Sans Pro', sans-serif;
      background: #ffffff;
      color: #1a2744;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-bar {{
      width: 100%;
      height: 8px;
      background: #1a2744;
      position: absolute;
      top: 0;
      left: 0;
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: #4a90d9;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 48px;
      font-weight: 700;
      margin-bottom: 12px;
    }}
    .subheadline {{
      font-size: 20px;
      color: #3d5a80;
      margin-bottom: 50px;
    }}
    .content {{
      display: flex;
      gap: 60px;
    }}
    .left {{
      flex: 1.2;
    }}
    .section-title {{
      font-size: 14px;
      font-weight: 600;
      color: #4a90d9;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 20px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th {{
      font-size: 11px;
      font-weight: 600;
      color: #8896a8;
      text-transform: uppercase;
      text-align: left;
      padding: 12px 0;
      border-bottom: 2px solid #1a2744;
    }}
    td {{
      padding: 16px 0;
      border-bottom: 1px solid #e8ecf2;
      vertical-align: middle;
    }}
    .alloc-category {{
      font-size: 16px;
      font-weight: 600;
    }}
    .alloc-amount {{
      font-size: 18px;
      font-weight: 700;
      color: #1a2744;
    }}
    .alloc-pct {{
      font-size: 14px;
      color: #4a90d9;
      font-weight: 600;
    }}
    .alloc-bar-cell {{
      width: 200px;
    }}
    .alloc-bar {{
      height: 8px;
      background: #e8ecf2;
      border-radius: 4px;
    }}
    .alloc-fill {{
      height: 100%;
      background: #1a2744;
      border-radius: 4px;
    }}
    .right {{
      flex: 0.8;
      background: #1a2744;
      color: white;
      padding: 40px;
    }}
    .right .section-title {{
      color: #4a90d9;
      margin-bottom: 28px;
    }}
    .phases {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .phase {{
      display: flex;
      gap: 16px;
      align-items: flex-start;
    }}
    .phase-num {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #4a90d9;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 13px;
      flex-shrink: 0;
    }}
    .phase-time {{
      font-size: 12px;
      color: rgba(255,255,255,0.5);
      margin-bottom: 4px;
    }}
    .phase-desc {{
      font-size: 15px;
      line-height: 1.4;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="content">
    <div class="left">
      <div class="section-title">Capital Allocation</div>
      <table>
        <thead><tr><th>Category</th><th>Amount</th><th>%</th><th>Allocation</th></tr></thead>
        <tbody>{table_rows}</tbody>
      </table>
    </div>
    <div class="right">
      <div class="section-title">Investment Timeline</div>
      <div class="phases">{phases_html}</div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # CONSUMER STYLE - Colorful bars with gradient
        # =====================================================================
        elif 'consumer' in style:
            # Build colorful fund cards
            colors = ["#ec4899", "#a855f7", "#8b5cf6", "#6366f1", "#3b82f6"]
            fund_cards = ""
            for i, item in enumerate(fund_items):
                color = colors[i % len(colors)]
                pct = item.get("percentage", 0)
                fund_cards += f'''
                <div class="fund-card">
                    <div class="fund-icon" style="background: {color};">💰</div>
                    <div class="fund-info">
                        <div class="fund-name">{item.get("label", "")}</div>
                        <div class="fund-amt">{item.get("amount", "")}</div>
                    </div>
                    <div class="fund-pct">{pct}%</div>
                    <div class="fund-bar">
                        <div class="fund-fill" style="width: {pct}%; background: {color};"></div>
                    </div>
                </div>'''

            # Build timeline with emojis
            timeline_html = ""
            emojis = ["🚀", "📈", "💪", "🎯", "✨", "🏆"]
            for i, m in enumerate(milestones):
                timeline_html += f'''
                <div class="milestone">
                    <div class="milestone-emoji">{emojis[i % len(emojis)]}</div>
                    <div class="milestone-content">
                        <div class="milestone-time">{m.get("month", "")}</div>
                        <div class="milestone-text">{m.get("text", "")}</div>
                    </div>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: linear-gradient(180deg, #fffbfc 0%, #fdf2f8 100%);
      color: #1f1f1f;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .blob {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.4;
    }}
    .blob-1 {{ width: 400px; height: 400px; background: #ec4899; top: -100px; right: 200px; }}
    .blob-2 {{ width: 300px; height: 300px; background: #a855f7; bottom: 100px; left: -50px; }}
    .main {{ position: relative; z-index: 1; }}
    .label {{
      display: inline-block;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      color: white;
      font-size: 13px;
      font-weight: 700;
      padding: 8px 20px;
      border-radius: 50px;
      margin-bottom: 24px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      margin-bottom: 12px;
    }}
    .subheadline {{
      font-size: 20px;
      color: #666;
      margin-bottom: 40px;
    }}
    .content {{
      display: flex;
      gap: 50px;
    }}
    .left {{
      flex: 1.2;
    }}
    .fund-cards {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .fund-card {{
      background: white;
      border-radius: 16px;
      padding: 20px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 4px 20px rgba(236, 72, 153, 0.1);
    }}
    .fund-icon {{
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }}
    .fund-info {{
      flex: 1;
    }}
    .fund-name {{
      font-size: 16px;
      font-weight: 600;
    }}
    .fund-amt {{
      font-size: 14px;
      color: #666;
    }}
    .fund-pct {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .fund-bar {{
      width: 150px;
      height: 8px;
      background: #fce7f3;
      border-radius: 4px;
    }}
    .fund-fill {{
      height: 100%;
      border-radius: 4px;
    }}
    .right {{
      flex: 0.8;
      background: white;
      border-radius: 24px;
      padding: 32px;
      box-shadow: 0 4px 24px rgba(236, 72, 153, 0.1);
    }}
    .timeline-title {{
      font-size: 14px;
      font-weight: 700;
      color: #ec4899;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 24px;
    }}
    .milestones {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .milestone {{
      display: flex;
      gap: 16px;
      align-items: flex-start;
    }}
    .milestone-emoji {{
      font-size: 24px;
    }}
    .milestone-time {{
      font-size: 12px;
      color: #999;
      margin-bottom: 4px;
    }}
    .milestone-text {{
      font-size: 15px;
      font-weight: 500;
    }}
  </style>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="main">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <p class="subheadline">{subheadline}</p>
    <div class="content">
      <div class="left">
        <div class="fund-cards">{fund_cards}</div>
      </div>
      <div class="right">
        <div class="timeline-title">Roadmap</div>
        <div class="milestones">{timeline_html}</div>
      </div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # CREATIVE STYLE - Bold asymmetric layout
        # =====================================================================
        elif 'creative' in style:
            # Build big allocation blocks
            alloc_blocks = ""
            for item in fund_items:
                pct = item.get("percentage", 0)
                alloc_blocks += f'''
                <div class="alloc-block">
                    <div class="alloc-pct">{pct}%</div>
                    <div class="alloc-details">
                        <div class="alloc-name">{item.get("label", "")}</div>
                        <div class="alloc-amt">{item.get("amount", "")}</div>
                    </div>
                </div>'''

            # Build vertical timeline
            timeline_html = ""
            for m in milestones:
                timeline_html += f'''
                <div class="step">
                    <div class="step-marker"></div>
                    <div class="step-content">
                        <span class="step-time">{m.get("month", "")}</span>
                        <span class="step-text">{m.get("text", "")}</span>
                    </div>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0f0f0f;
      color: #f5f5f5;
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .sidebar {{
      width: 100px;
      background: #facc15;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 4px;
      color: #0f0f0f;
    }}
    .main {{
      flex: 1;
      padding: 80px;
    }}
    .label {{
      font-size: 13px;
      font-weight: 800;
      color: #facc15;
      text-transform: uppercase;
      letter-spacing: 3px;
      margin-bottom: 24px;
    }}
    .headline {{
      font-size: 60px;
      font-weight: 900;
      line-height: 1.0;
      margin-bottom: 12px;
      max-width: 800px;
    }}
    .subheadline {{
      font-size: 20px;
      color: rgba(255,255,255,0.5);
      margin-bottom: 50px;
    }}
    .content {{
      display: flex;
      gap: 60px;
    }}
    .left {{
      flex: 1.2;
    }}
    .alloc-blocks {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .alloc-block {{
      background: #1a1a1a;
      padding: 24px 28px;
      display: flex;
      align-items: center;
      gap: 24px;
    }}
    .alloc-pct {{
      font-size: 48px;
      font-weight: 900;
      color: #facc15;
      min-width: 100px;
    }}
    .alloc-name {{
      font-size: 18px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .alloc-amt {{
      font-size: 14px;
      color: rgba(255,255,255,0.5);
      margin-top: 4px;
    }}
    .right {{
      flex: 0.8;
      padding-left: 40px;
      border-left: 3px solid #333;
    }}
    .timeline-title {{
      font-size: 13px;
      font-weight: 800;
      color: #facc15;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 32px;
    }}
    .steps {{
      display: flex;
      flex-direction: column;
      gap: 24px;
      position: relative;
      padding-left: 32px;
    }}
    .steps::before {{
      content: '';
      position: absolute;
      left: 8px;
      top: 0;
      bottom: 0;
      width: 3px;
      background: #333;
    }}
    .step {{
      position: relative;
    }}
    .step-marker {{
      width: 20px;
      height: 20px;
      position: absolute;
      left: -32px;
      background: #facc15;
    }}
    .step-time {{
      font-size: 12px;
      color: rgba(255,255,255,0.4);
      margin-right: 12px;
    }}
    .step-text {{
      font-size: 16px;
      font-weight: 500;
    }}
  </style>
</head>
<body>
  <div class="sidebar"><span class="sidebar-text">Investment</span></div>
  <div class="main">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <p class="subheadline">{subheadline}</p>
    <div class="content">
      <div class="left">
        <div class="alloc-blocks">{alloc_blocks}</div>
      </div>
      <div class="right">
        <div class="timeline-title">Deployment Plan</div>
        <div class="steps">{timeline_html}</div>
      </div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # MINIMAL STYLE - Clean, understated bars
        # =====================================================================
        elif 'minimal' in style:
            # Build minimal allocation list
            alloc_list = ""
            for item in fund_items:
                pct = item.get("percentage", 0)
                alloc_list += f'''
                <div class="alloc-row">
                    <span class="alloc-label">{item.get("label", "")}</span>
                    <span class="alloc-amt">{item.get("amount", "")}</span>
                    <div class="alloc-bar">
                        <div class="alloc-fill" style="width: {pct}%;"></div>
                    </div>
                </div>'''

            # Build minimal timeline
            timeline_html = ""
            for m in milestones:
                timeline_html += f'''
                <div class="milestone">
                    <div class="milestone-time">{m.get("month", "")}</div>
                    <div class="milestone-text">{m.get("text", "")}</div>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #fafafa;
      color: #171717;
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
    }}
    .label {{
      font-size: 12px;
      font-weight: 500;
      color: #a3a3a3;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 44px;
      font-weight: 300;
      letter-spacing: -0.02em;
      margin-bottom: 12px;
    }}
    .subheadline {{
      font-size: 18px;
      color: #737373;
      margin-bottom: 60px;
    }}
    .content {{
      display: flex;
      gap: 100px;
    }}
    .left {{
      flex: 1.2;
    }}
    .section-label {{
      font-size: 11px;
      font-weight: 500;
      color: #a3a3a3;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 28px;
    }}
    .allocs {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .alloc-row {{
      display: grid;
      grid-template-columns: 1fr 100px 200px;
      gap: 24px;
      align-items: center;
      padding-bottom: 20px;
      border-bottom: 1px solid #e5e5e5;
    }}
    .alloc-label {{
      font-size: 16px;
      font-weight: 500;
    }}
    .alloc-amt {{
      font-size: 16px;
      color: #737373;
      text-align: right;
    }}
    .alloc-bar {{
      height: 6px;
      background: #e5e5e5;
      border-radius: 3px;
    }}
    .alloc-fill {{
      height: 100%;
      background: #171717;
      border-radius: 3px;
    }}
    .right {{
      flex: 0.8;
    }}
    .milestones {{
      display: flex;
      flex-direction: column;
      gap: 0;
    }}
    .milestone {{
      display: flex;
      gap: 32px;
      padding: 20px 0;
      border-bottom: 1px solid #e5e5e5;
    }}
    .milestone-time {{
      font-size: 13px;
      color: #a3a3a3;
      width: 60px;
      flex-shrink: 0;
    }}
    .milestone-text {{
      font-size: 15px;
      color: #404040;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="content">
    <div class="left">
      <div class="section-label">Allocation</div>
      <div class="allocs">{alloc_list}</div>
    </div>
    <div class="right">
      <div class="section-label">Timeline</div>
      <div class="milestones">{timeline_html}</div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # SALES STYLE - ROI and growth focused
        # =====================================================================
        elif 'sales' in style:
            # Build investment cards
            investment_cards = ""
            for item in fund_items:
                pct = item.get("percentage", 0)
                investment_cards += f'''
                <div class="inv-card">
                    <div class="inv-bar">
                        <div class="inv-fill" style="height: {pct}%;"></div>
                    </div>
                    <div class="inv-pct">{pct}%</div>
                    <div class="inv-label">{item.get("label", "")}</div>
                    <div class="inv-amt">{item.get("amount", "")}</div>
                </div>'''

            # Build ROI milestones
            milestones_html = ""
            for m in milestones:
                milestones_html += f'''
                <div class="roi-item">
                    <div class="roi-icon">→</div>
                    <div class="roi-content">
                        <div class="roi-time">{m.get("month", "")}</div>
                        <div class="roi-text">{m.get("text", "")}</div>
                    </div>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0c1929;
      color: #ffffff;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .label {{
      font-size: 13px;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      margin-bottom: 12px;
    }}
    .subheadline {{
      font-size: 20px;
      color: rgba(255,255,255,0.6);
      margin-bottom: 50px;
    }}
    .content {{
      display: flex;
      gap: 50px;
    }}
    .left {{
      flex: 1.3;
    }}
    .inv-cards {{
      display: flex;
      gap: 20px;
      height: 350px;
      align-items: flex-end;
    }}
    .inv-card {{
      flex: 1;
      background: #132337;
      border-radius: 12px;
      padding: 24px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .inv-bar {{
      width: 40px;
      height: 180px;
      background: #1e3a5f;
      border-radius: 6px;
      position: relative;
      overflow: hidden;
      margin-bottom: 16px;
    }}
    .inv-fill {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(180deg, #10b981 0%, #059669 100%);
      border-radius: 6px;
    }}
    .inv-pct {{
      font-size: 28px;
      font-weight: 800;
      color: #10b981;
    }}
    .inv-label {{
      font-size: 14px;
      font-weight: 600;
      margin-top: 8px;
    }}
    .inv-amt {{
      font-size: 13px;
      color: rgba(255,255,255,0.5);
      margin-top: 4px;
    }}
    .right {{
      flex: 0.7;
      background: #132337;
      border-radius: 16px;
      padding: 32px;
    }}
    .roi-title {{
      font-size: 14px;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 28px;
    }}
    .roi-items {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .roi-item {{
      display: flex;
      gap: 16px;
      align-items: flex-start;
    }}
    .roi-icon {{
      color: #10b981;
      font-weight: 700;
      font-size: 18px;
    }}
    .roi-time {{
      font-size: 12px;
      color: rgba(255,255,255,0.4);
      margin-bottom: 4px;
    }}
    .roi-text {{
      font-size: 15px;
      line-height: 1.4;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <p class="subheadline">{subheadline}</p>
  <div class="content">
    <div class="left">
      <div class="inv-cards">{investment_cards}</div>
    </div>
    <div class="right">
      <div class="roi-title">Expected Returns</div>
      <div class="roi-items">{milestones_html}</div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # DEFAULT/TECH STYLE - Modern tech aesthetic
        # =====================================================================
        funds_html = "\n".join(f'''
        <div class="fund-item">
          <div class="fund-header">
            <span class="fund-label">{item.get("label", "")}</span>
            <span class="fund-amount">{item.get("amount", "")}</span>
          </div>
          <div class="fund-bar">
            <div class="fund-fill" style="width: {item.get("percentage", 0)}%;"></div>
          </div>
        </div>''' for item in fund_items)

        milestones_html = "\n".join(f'''
        <div class="milestone">
          <div class="milestone-month">{m.get("month", "")}</div>
          <div class="milestone-text">{m.get("text", "")}</div>
        </div>''' for m in milestones)

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - {label}</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      padding: {theme.slide_padding};
    }}
    .left {{
      flex: 1;
      display: flex;
      flex-direction: column;
      padding-right: 80px;
    }}
    .right {{
      flex: 1;
      background: #000;
      color: #fff;
      border-radius: {theme.radius_large};
      padding: 48px;
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 48px;
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      margin-bottom: 16px;
    }}
    .subheadline {{
      font-size: 20px;
      color: {theme.text_secondary};
      margin-bottom: 48px;
    }}
    .fund-items {{
      display: flex;
      flex-direction: column;
      gap: 28px;
    }}
    .fund-item {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .fund-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .fund-label {{
      font-size: 18px;
      font-weight: {theme.font_weight_semibold};
    }}
    .fund-amount {{
      font-size: 18px;
      color: {theme.text_secondary};
    }}
    .fund-bar {{
      height: 8px;
      background: {theme.surface};
      border-radius: 4px;
      overflow: hidden;
    }}
    .fund-fill {{
      height: 100%;
      background: {theme.gradient_primary};
      border-radius: 4px;
    }}
    .right-label {{
      font-size: {theme.font_size_label};
      color: rgba(255,255,255,0.5);
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .milestones {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .milestone {{
      display: flex;
      align-items: flex-start;
      gap: 24px;
    }}
    .milestone-month {{
      font-size: 14px;
      font-weight: {theme.font_weight_semibold};
      color: rgba(255,255,255,0.5);
      min-width: 80px;
    }}
    .milestone-text {{
      font-size: 18px;
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <div class="left">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <p class="subheadline">{subheadline}</p>
    <div class="fund-items">
      {funds_html}
    </div>
  </div>
  <div class="right">
    <div class="right-label">12-Month Plan</div>
    <div class="milestones">
      {milestones_html}
    </div>
  </div>
</body>
</html>'''

    @staticmethod
    def render_image_slide(
        image_url: str,
        caption: Optional[str] = None,
        layout: str = "full",
        theme: Optional[Theme] = None,
    ) -> str:
        """Slide with prominent image."""
        theme = theme or LightTheme()

        caption_html = ""
        if caption:
            caption_html = f'<div class="caption">{caption}</div>'

        if layout == "full":
            img_style = "width: 100%; height: 100%; object-fit: cover;"
        elif layout == "centered":
            img_style = "max-width: 80%; max-height: 80%; object-fit: contain;"
        else:
            img_style = "max-width: 70%; object-fit: contain;"

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Image</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: {'0' if layout == 'full' else '80px'};
    }}
    .image {{
      {img_style}
    }}
    .caption {{
      margin-top: 32px;
      font-size: 18px;
      color: {theme.text_muted};
      text-align: center;
    }}
  </style>
</head>
<body>
  <img src="{image_url}" alt="Slide image" class="image">
  {caption_html}
</body>
</html>'''

    @staticmethod
    def render_pricing_slide(
        headline: str,
        tiers: List[Dict[str, Any]],
        label: str = "Business Model",
        unit_economics: Optional[Dict[str, Any]] = None,
        highlight_tier: Optional[int] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render pricing slide with style-specific layouts.
        tiers: List of {"name": str, "price": str, "period": str, "features": List[str]}
        unit_economics: {"items": [{"label": str, "value": str, "description": str}]}
        highlight_tier: Index of tier to highlight (0-based)
        """
        theme = theme or LightTheme()
        highlight_tier = highlight_tier if highlight_tier is not None else 1
        style = getattr(theme, 'name', 'light')

        # CONSULTING STYLE - Structured table-like layout
        if 'consulting' in style:
            tiers_html = ""
            for i, tier in enumerate(tiers):
                is_highlighted = i == highlight_tier
                border_class = "highlighted" if is_highlighted else ""
                features_html = "".join(f'<li>{f}</li>' for f in tier.get("features", []))
                tiers_html += f'''
                <div class="tier {border_class}">
                  <div class="tier-name">{tier.get("name", "")}</div>
                  <div class="tier-price">{tier.get("price", "")}</div>
                  <div class="tier-period">per {tier.get("period", "month")}</div>
                  <ul class="tier-features">{features_html}</ul>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Pricing</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 6px; background: {theme.accent}; }}
    .label {{ font-size: 12px; font-weight: 600; color: {theme.accent}; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 24px; }}
    .headline {{ font-family: {theme.headline_font_family}; font-size: 48px; font-weight: 600; margin-bottom: 60px; }}
    .tiers {{ display: flex; gap: 32px; }}
    .tier {{ flex: 1; padding: 40px; background: {theme.surface}; border-left: 4px solid {theme.border}; }}
    .tier.highlighted {{ border-left-color: {theme.accent}; }}
    .tier-name {{ font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: {theme.text_muted}; margin-bottom: 16px; }}
    .tier-price {{ font-family: {theme.headline_font_family}; font-size: 48px; font-weight: 600; }}
    .tier-period {{ font-size: 14px; color: {theme.text_muted}; margin-bottom: 32px; }}
    .tier-features {{ list-style: none; font-size: 15px; line-height: 2; color: {theme.text_secondary}; }}
    .tier-features li::before {{ content: "—"; margin-right: 12px; color: {theme.accent}; }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="tiers">{tiers_html}</div>
</body>
</html>'''

        # CONSUMER STYLE - Colorful cards with gradients
        elif 'consumer' in style:
            tiers_html = ""
            for i, tier in enumerate(tiers):
                is_highlighted = i == highlight_tier
                card_style = f"background: {theme.gradient_primary}; color: white;" if is_highlighted else f"background: {theme.surface}; border: 2px solid {theme.border};"
                features_html = "".join(f'<li>{f}</li>' for f in tier.get("features", []))
                badge = '<div class="badge">Best Value</div>' if is_highlighted else ""
                tiers_html += f'''
                <div class="tier" style="{card_style}">
                  {badge}
                  <div class="tier-name">{tier.get("name", "")}</div>
                  <div class="tier-price">{tier.get("price", "")}</div>
                  <div class="tier-period">/{tier.get("period", "month")}</div>
                  <ul class="tier-features">{features_html}</ul>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Pricing</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; padding: 80px 100px; position: relative; overflow: hidden; }}
    .gradient-blob {{ position: absolute; width: 600px; height: 600px; border-radius: 50%; background: {theme.gradient_primary}; opacity: 0.1; filter: blur(80px); bottom: -200px; left: -100px; }}
    .label {{ display: inline-block; background: {theme.accent}; color: white; padding: 8px 20px; border-radius: 100px; font-size: 13px; font-weight: 600; text-transform: uppercase; margin-bottom: 32px; }}
    .headline {{ font-size: 52px; font-weight: 800; margin-bottom: 50px; background: {theme.gradient_text}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .tiers {{ display: flex; gap: 28px; }}
    .tier {{ flex: 1; padding: 40px; border-radius: 28px; position: relative; text-align: center; }}
    .badge {{ position: absolute; top: -14px; left: 50%; transform: translateX(-50%); background: {theme.background}; color: {theme.accent}; padding: 8px 20px; border-radius: 100px; font-size: 12px; font-weight: 700; border: 2px solid {theme.accent}; }}
    .tier-name {{ font-size: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.8; margin-bottom: 16px; }}
    .tier-price {{ font-size: 56px; font-weight: 900; }}
    .tier-period {{ font-size: 16px; opacity: 0.7; margin-bottom: 28px; }}
    .tier-features {{ list-style: none; font-size: 15px; line-height: 2.2; text-align: left; }}
    .tier-features li::before {{ content: "✓"; margin-right: 12px; }}
  </style>
</head>
<body>
  <div class="gradient-blob"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="tiers">{tiers_html}</div>
</body>
</html>'''

        # CREATIVE STYLE - Bold asymmetric
        elif 'creative' in style:
            tiers_html = ""
            for i, tier in enumerate(tiers):
                is_highlighted = i == highlight_tier
                bg = f"background: {theme.accent}; color: {theme.background};" if is_highlighted else ""
                features_html = "".join(f'<li>{f}</li>' for f in tier.get("features", []))
                tiers_html += f'''
                <div class="tier" style="{bg}">
                  <div class="tier-name">{tier.get("name", "")}</div>
                  <div class="tier-price">{tier.get("price", "")}</div>
                  <ul class="tier-features">{features_html}</ul>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Pricing</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; display: grid; grid-template-columns: 100px 1fr; }}
    .sidebar {{ background: {theme.accent}; display: flex; align-items: center; justify-content: center; }}
    .sidebar-text {{ writing-mode: vertical-rl; transform: rotate(180deg); font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.2em; color: {theme.background}; }}
    .main {{ padding: 80px 100px; }}
    .headline {{ font-size: 64px; font-weight: 900; margin-bottom: 60px; }}
    .tiers {{ display: flex; gap: 32px; }}
    .tier {{ flex: 1; padding: 48px; border-left: 5px solid {theme.accent}; }}
    .tier-name {{ font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 20px; opacity: 0.6; }}
    .tier-price {{ font-size: 72px; font-weight: 900; margin-bottom: 32px; }}
    .tier-features {{ list-style: none; font-size: 16px; line-height: 2; }}
    .tier-features li {{ padding: 8px 0; border-bottom: 1px solid currentColor; opacity: 0.3; }}
  </style>
</head>
<body>
  <div class="sidebar"><div class="sidebar-text">{label}</div></div>
  <div class="main">
    <h1 class="headline">{headline}</h1>
    <div class="tiers">{tiers_html}</div>
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Clean, elegant
        elif 'minimal' in style:
            tiers_html = ""
            for i, tier in enumerate(tiers):
                features_html = "".join(f'<li>{f}</li>' for f in tier.get("features", []))
                tiers_html += f'''
                <div class="tier">
                  <div class="tier-name">{tier.get("name", "")}</div>
                  <div class="tier-price">{tier.get("price", "")}<span class="tier-period">/{tier.get("period", "mo")}</span></div>
                  <ul class="tier-features">{features_html}</ul>
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Pricing</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; padding: 120px 160px; }}
    .label {{ font-size: 11px; font-weight: 500; color: {theme.text_muted}; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 48px; }}
    .headline {{ font-size: 40px; font-weight: 400; margin-bottom: 80px; letter-spacing: -0.02em; }}
    .tiers {{ display: flex; gap: 80px; }}
    .tier {{ flex: 1; }}
    .tier-name {{ font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.1em; color: {theme.text_muted}; margin-bottom: 24px; }}
    .tier-price {{ font-size: 48px; font-weight: 300; margin-bottom: 40px; }}
    .tier-period {{ font-size: 16px; font-weight: 300; color: {theme.text_muted}; }}
    .tier-features {{ list-style: none; font-size: 15px; font-weight: 300; line-height: 2.2; color: {theme.text_secondary}; }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="tiers">{tiers_html}</div>
</body>
</html>'''

        # SALES STYLE - CTA focused, high contrast
        elif 'sales' in style:
            tiers_html = ""
            for i, tier in enumerate(tiers):
                is_highlighted = i == highlight_tier
                card_class = "highlighted" if is_highlighted else ""
                features_html = "".join(f'<li>✓ {f}</li>' for f in tier.get("features", []))
                cta = '<div class="cta">Start Free Trial →</div>' if is_highlighted else '<div class="cta-secondary">Get Started</div>'
                tiers_html += f'''
                <div class="tier {card_class}">
                  <div class="tier-name">{tier.get("name", "")}</div>
                  <div class="tier-price">{tier.get("price", "")}<span class="tier-period">/{tier.get("period", "mo")}</span></div>
                  <ul class="tier-features">{features_html}</ul>
                  {cta}
                </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide - Pricing</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {theme.body_font_family}; background: {theme.background}; color: {theme.text_primary}; width: 1920px; height: 1080px; padding: 80px 100px; }}
    .label {{ display: inline-block; background: #ecfdf5; color: #059669; padding: 8px 16px; border-radius: 6px; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 32px; }}
    .headline {{ font-size: 48px; font-weight: 800; margin-bottom: 50px; }}
    .tiers {{ display: flex; gap: 28px; }}
    .tier {{ flex: 1; padding: 40px; border-radius: 16px; background: {theme.surface}; border: 2px solid {theme.border}; display: flex; flex-direction: column; }}
    .tier.highlighted {{ border-color: {theme.accent}; box-shadow: 0 8px 32px rgba(16,185,129,0.15); }}
    .tier-name {{ font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {theme.text_muted}; margin-bottom: 16px; }}
    .tier-price {{ font-size: 52px; font-weight: 800; }}
    .tier-period {{ font-size: 16px; font-weight: 400; color: {theme.text_muted}; }}
    .tier-features {{ list-style: none; font-size: 15px; line-height: 2; color: {theme.text_secondary}; flex: 1; margin: 28px 0; }}
    .tier-features li {{ color: {theme.text_secondary}; }}
    .cta {{ background: {theme.accent}; color: white; padding: 14px 24px; border-radius: 8px; font-weight: 600; text-align: center; }}
    .cta-secondary {{ border: 2px solid {theme.border}; padding: 14px 24px; border-radius: 8px; font-weight: 600; text-align: center; color: {theme.text_secondary}; }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="tiers">{tiers_html}</div>
</body>
</html>'''

        # DEFAULT/TECH STYLE
        highlight_tier = highlight_tier if highlight_tier is not None else 1

        tiers_html = ""
        for i, tier in enumerate(tiers):
            is_highlighted = i == highlight_tier
            border_style = f"border: 2px solid {theme.accent};" if is_highlighted else f"border: 2px solid {theme.border};"
            bg_style = f"background: {theme.surface};" if is_highlighted else ""
            badge_html = '<div class="popular-badge">Most Popular</div>' if is_highlighted else ""

            features_html = "\n".join(
                f'<li>{feature}</li>' for feature in tier.get("features", [])
            )

            tiers_html += f'''
            <div class="tier" style="{border_style} {bg_style}">
                {badge_html}
                <div class="tier-name">{tier.get("name", "")}</div>
                <div class="tier-price">{tier.get("price", "")}<span class="tier-period">/{tier.get("period", "month")}</span></div>
                <ul class="tier-features">{features_html}</ul>
            </div>
            '''

        unit_econ_html = ""
        if unit_economics:
            items_html = ""
            for item in unit_economics.get("items", []):
                items_html += f'''
                <div class="unit-item">
                    <div class="unit-value">{item.get("value", "")}</div>
                    <div class="unit-label">{item.get("label", "")}</div>
                    <div class="unit-desc">{item.get("description", "")}</div>
                </div>
                '''
            unit_econ_html = f'''
            <div class="unit-economics">
                <div class="unit-economics-title">Unit Economics</div>
                <div class="unit-items">{items_html}</div>
            </div>
            '''

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Pricing</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 60px;
    }}
    .tiers {{
      display: flex;
      gap: 32px;
      margin-bottom: 48px;
    }}
    .tier {{
      flex: 1;
      padding: 40px;
      border-radius: 16px;
      position: relative;
    }}
    .popular-badge {{
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: {theme.accent};
      color: white;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
    }}
    .tier-name {{
      font-size: 18px;
      font-weight: 600;
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 16px;
    }}
    .tier-price {{
      font-size: 56px;
      font-weight: 800;
      margin-bottom: 24px;
    }}
    .tier-period {{
      font-size: 20px;
      font-weight: 400;
      color: {theme.text_muted};
    }}
    .tier-features {{
      list-style: none;
      font-size: 16px;
      line-height: 2;
      color: {theme.text_secondary};
    }}
    .tier-features li::before {{
      content: "✓";
      margin-right: 12px;
      color: {theme.accent};
    }}
    .unit-economics {{
      background: {theme.surface};
      padding: 40px;
      border-radius: 16px;
    }}
    .unit-economics-title {{
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 32px;
    }}
    .unit-items {{
      display: flex;
      gap: 60px;
    }}
    .unit-item {{
      flex: 1;
    }}
    .unit-value {{
      font-size: 48px;
      font-weight: 800;
      color: {theme.accent};
      margin-bottom: 8px;
    }}
    .unit-label {{
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 4px;
    }}
    .unit-desc {{
      font-size: 14px;
      color: {theme.text_muted};
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="tiers">{tiers_html}</div>
  {unit_econ_html}
</body>
</html>'''

    @staticmethod
    def render_traction_slide(
        headline: str,
        label: str = "Traction",
        status_box: Optional[Dict[str, Any]] = None,
        milestones: Optional[List[Dict[str, Any]]] = None,
        metrics: Optional[List[Dict[str, Any]]] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render traction/status slide with style-specific layouts.
        Pattern from: runit-pitch/slide-09-traction.html

        status_box: {"title": str, "items": [{"label": str, "value": str, "change": str}]}
        milestones: [{"date": str, "title": str, "status": "done"|"current"|"upcoming"}]
        metrics: [{"value": str, "label": str, "trend": str}]
        """
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        # =====================================================================
        # CONSULTING STYLE - Structured progress table, numbered phases
        # =====================================================================
        if 'consulting' in style:
            # Build status table
            status_rows = ""
            if status_box:
                for item in status_box.get("items", []):
                    change = item.get("change", "")
                    change_class = "up" if "+" in change or "↑" in change else "down" if "-" in change or "↓" in change else ""
                    status_rows += f'''
                    <tr>
                        <td class="metric-name">{item.get("label", "")}</td>
                        <td class="metric-value">{item.get("value", "")}</td>
                        <td class="metric-change {change_class}">{change}</td>
                    </tr>'''

            # Build milestone phases
            phases_html = ""
            if milestones:
                for i, m in enumerate(milestones, 1):
                    status = m.get("status", "upcoming")
                    status_class = "complete" if status == "done" else "active" if status == "current" else "pending"
                    phases_html += f'''
                    <div class="phase {status_class}">
                        <div class="phase-num">{i}</div>
                        <div class="phase-info">
                            <div class="phase-date">{m.get("date", "")}</div>
                            <div class="phase-title">{m.get("title", "")}</div>
                        </div>
                        <div class="phase-status">{"✓" if status == "done" else "●" if status == "current" else "○"}</div>
                    </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Source Sans Pro', sans-serif;
      background: #ffffff;
      color: #1a2744;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .top-bar {{
      width: 100%;
      height: 8px;
      background: #1a2744;
      position: absolute;
      top: 0;
      left: 0;
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: #4a90d9;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 48px;
      font-weight: 700;
      margin-bottom: 50px;
    }}
    .content {{
      display: flex;
      gap: 60px;
    }}
    .left-section {{
      flex: 1;
    }}
    .section-title {{
      font-size: 14px;
      font-weight: 600;
      color: #4a90d9;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 20px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      padding: 16px 0;
      text-align: left;
      border-bottom: 1px solid #e8ecf2;
    }}
    th {{
      font-size: 12px;
      font-weight: 600;
      color: #8896a8;
      text-transform: uppercase;
    }}
    .metric-name {{
      font-size: 16px;
      color: #3d5a80;
    }}
    .metric-value {{
      font-size: 24px;
      font-weight: 700;
      color: #1a2744;
    }}
    .metric-change {{
      font-size: 14px;
      font-weight: 600;
    }}
    .metric-change.up {{ color: #059669; }}
    .metric-change.down {{ color: #dc2626; }}
    .right-section {{
      flex: 1;
    }}
    .phases {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .phase {{
      display: flex;
      align-items: center;
      gap: 20px;
      padding: 20px;
      background: #f5f7fa;
      border-left: 4px solid #d1d9e6;
    }}
    .phase.complete {{
      border-left-color: #059669;
      background: #f0fdf4;
    }}
    .phase.active {{
      border-left-color: #4a90d9;
      background: #eff6ff;
    }}
    .phase-num {{
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #1a2744;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 14px;
    }}
    .phase.complete .phase-num {{ background: #059669; }}
    .phase.active .phase-num {{ background: #4a90d9; }}
    .phase-info {{ flex: 1; }}
    .phase-date {{
      font-size: 12px;
      color: #8896a8;
      margin-bottom: 4px;
    }}
    .phase-title {{
      font-size: 16px;
      font-weight: 600;
    }}
    .phase.pending .phase-title {{ color: #8896a8; }}
    .phase-status {{
      font-size: 18px;
      color: #1a2744;
    }}
    .phase.complete .phase-status {{ color: #059669; }}
    .phase.active .phase-status {{ color: #4a90d9; }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="content">
    <div class="left-section">
      <div class="section-title">{status_box.get("title", "Key Metrics") if status_box else "Key Metrics"}</div>
      <table>
        <thead><tr><th>Metric</th><th>Value</th><th>Change</th></tr></thead>
        <tbody>{status_rows}</tbody>
      </table>
    </div>
    <div class="right-section">
      <div class="section-title">Roadmap Progress</div>
      <div class="phases">{phases_html}</div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # CONSUMER STYLE - Celebration-oriented, colorful progress
        # =====================================================================
        elif 'consumer' in style:
            # Build celebration metrics
            metrics_cards = ""
            if status_box:
                icons = ["📈", "💰", "👥", "⭐", "🚀", "💎"]
                for i, item in enumerate(status_box.get("items", [])):
                    change = item.get("change", "")
                    is_positive = "+" in change or "↑" in change
                    metrics_cards += f'''
                    <div class="stat-card">
                        <div class="stat-icon">{icons[i % len(icons)]}</div>
                        <div class="stat-value">{item.get("value", "")}</div>
                        <div class="stat-label">{item.get("label", "")}</div>
                        <div class="stat-change {"positive" if is_positive else ""}">{change}</div>
                    </div>'''

            # Build timeline
            timeline_html = ""
            if milestones:
                for m in milestones:
                    status = m.get("status", "upcoming")
                    emoji = "✨" if status == "done" else "🔥" if status == "current" else "🎯"
                    timeline_html += f'''
                    <div class="timeline-item {status}">
                        <div class="timeline-emoji">{emoji}</div>
                        <div class="timeline-dot"></div>
                        <div class="timeline-content">
                            <div class="timeline-date">{m.get("date", "")}</div>
                            <div class="timeline-title">{m.get("title", "")}</div>
                        </div>
                    </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: linear-gradient(180deg, #fffbfc 0%, #fdf2f8 100%);
      color: #1f1f1f;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      position: relative;
      overflow: hidden;
    }}
    .blob {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.4;
    }}
    .blob-1 {{ width: 400px; height: 400px; background: #ec4899; top: -100px; right: 200px; }}
    .blob-2 {{ width: 300px; height: 300px; background: #a855f7; bottom: 100px; left: -50px; }}
    .main {{ position: relative; z-index: 1; }}
    .label {{
      display: inline-block;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      color: white;
      font-size: 13px;
      font-weight: 700;
      padding: 8px 20px;
      border-radius: 50px;
      margin-bottom: 24px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      margin-bottom: 50px;
    }}
    .stats-grid {{
      display: flex;
      gap: 24px;
      margin-bottom: 50px;
    }}
    .stat-card {{
      flex: 1;
      background: white;
      border-radius: 24px;
      padding: 28px;
      text-align: center;
      box-shadow: 0 4px 24px rgba(236, 72, 153, 0.1);
    }}
    .stat-icon {{
      font-size: 32px;
      margin-bottom: 12px;
    }}
    .stat-value {{
      font-size: 36px;
      font-weight: 800;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .stat-label {{
      font-size: 14px;
      color: #666;
      margin-top: 8px;
    }}
    .stat-change {{
      font-size: 13px;
      font-weight: 600;
      color: #999;
      margin-top: 8px;
    }}
    .stat-change.positive {{
      color: #22c55e;
    }}
    .timeline {{
      display: flex;
      gap: 0;
      position: relative;
    }}
    .timeline::before {{
      content: '';
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      height: 4px;
      background: #fce7f3;
      transform: translateY(-50%);
    }}
    .timeline-item {{
      flex: 1;
      text-align: center;
      position: relative;
      padding-top: 40px;
    }}
    .timeline-emoji {{
      font-size: 28px;
      margin-bottom: 16px;
    }}
    .timeline-dot {{
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #fce7f3;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      margin-top: 20px;
    }}
    .timeline-item.done .timeline-dot {{
      background: linear-gradient(135deg, #ec4899, #a855f7);
    }}
    .timeline-item.current .timeline-dot {{
      background: #ec4899;
      box-shadow: 0 0 0 6px rgba(236, 72, 153, 0.3);
    }}
    .timeline-content {{
      margin-top: 50px;
    }}
    .timeline-date {{
      font-size: 13px;
      color: #999;
      margin-bottom: 6px;
    }}
    .timeline-title {{
      font-size: 15px;
      font-weight: 600;
    }}
    .timeline-item.upcoming .timeline-title {{
      color: #999;
    }}
  </style>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="main">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="stats-grid">{metrics_cards}</div>
    <div class="timeline">{timeline_html}</div>
  </div>
</body>
</html>'''

        # =====================================================================
        # CREATIVE STYLE - Bold asymmetric, accent sidebar
        # =====================================================================
        elif 'creative' in style:
            # Build big number metrics
            big_metrics = ""
            if status_box:
                for item in status_box.get("items", []):
                    change = item.get("change", "")
                    big_metrics += f'''
                    <div class="big-metric">
                        <div class="big-value">{item.get("value", "")}</div>
                        <div class="big-label">{item.get("label", "")}</div>
                        <div class="big-change">{change}</div>
                    </div>'''

            # Build vertical timeline
            timeline_html = ""
            if milestones:
                for m in milestones:
                    status = m.get("status", "upcoming")
                    timeline_html += f'''
                    <div class="step {status}">
                        <div class="step-marker"></div>
                        <div class="step-content">
                            <span class="step-date">{m.get("date", "")}</span>
                            <span class="step-title">{m.get("title", "")}</span>
                        </div>
                    </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0f0f0f;
      color: #f5f5f5;
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .sidebar {{
      width: 100px;
      background: #facc15;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 4px;
      color: #0f0f0f;
    }}
    .main {{
      flex: 1;
      padding: 80px;
      display: flex;
      flex-direction: column;
    }}
    .label {{
      font-size: 13px;
      font-weight: 800;
      color: #facc15;
      text-transform: uppercase;
      letter-spacing: 3px;
      margin-bottom: 24px;
    }}
    .headline {{
      font-size: 60px;
      font-weight: 900;
      line-height: 1.0;
      margin-bottom: 60px;
      max-width: 800px;
    }}
    .content {{
      display: flex;
      gap: 80px;
      flex: 1;
    }}
    .metrics-section {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 32px;
    }}
    .big-metric {{
      background: #1a1a1a;
      padding: 32px;
    }}
    .big-value {{
      font-size: 64px;
      font-weight: 900;
      color: #facc15;
    }}
    .big-label {{
      font-size: 16px;
      font-weight: 600;
      color: rgba(255,255,255,0.6);
      margin-top: 8px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    .big-change {{
      font-size: 18px;
      font-weight: 800;
      color: #22c55e;
      margin-top: 12px;
    }}
    .timeline-section {{
      flex: 1;
    }}
    .steps {{
      display: flex;
      flex-direction: column;
      gap: 24px;
      position: relative;
      padding-left: 40px;
    }}
    .steps::before {{
      content: '';
      position: absolute;
      left: 12px;
      top: 0;
      bottom: 0;
      width: 3px;
      background: #333;
    }}
    .step {{
      position: relative;
    }}
    .step-marker {{
      width: 28px;
      height: 28px;
      position: absolute;
      left: -40px;
      background: #333;
    }}
    .step.done .step-marker {{
      background: #facc15;
    }}
    .step.current .step-marker {{
      background: #facc15;
      box-shadow: 0 0 0 6px rgba(250, 204, 21, 0.3);
    }}
    .step-content {{
      padding: 16px 0;
    }}
    .step-date {{
      font-size: 13px;
      color: rgba(255,255,255,0.4);
      margin-right: 16px;
    }}
    .step-title {{
      font-size: 18px;
      font-weight: 600;
    }}
    .step.upcoming .step-title {{
      color: rgba(255,255,255,0.4);
    }}
  </style>
</head>
<body>
  <div class="sidebar"><span class="sidebar-text">Traction</span></div>
  <div class="main">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    <div class="content">
      <div class="metrics-section">{big_metrics}</div>
      <div class="timeline-section"><div class="steps">{timeline_html}</div></div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # MINIMAL STYLE - Clean, understated progress
        # =====================================================================
        elif 'minimal' in style:
            # Build minimal metrics
            metrics_html_items = ""
            if status_box:
                for item in status_box.get("items", []):
                    metrics_html_items += f'''
                    <div class="metric-row">
                        <span class="metric-label">{item.get("label", "")}</span>
                        <span class="metric-value">{item.get("value", "")}</span>
                    </div>'''

            # Build minimal timeline
            timeline_html = ""
            if milestones:
                for m in milestones:
                    status = m.get("status", "upcoming")
                    timeline_html += f'''
                    <div class="milestone {status}">
                        <div class="milestone-date">{m.get("date", "")}</div>
                        <div class="milestone-title">{m.get("title", "")}</div>
                    </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #fafafa;
      color: #171717;
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
    }}
    .label {{
      font-size: 12px;
      font-weight: 500;
      color: #a3a3a3;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 44px;
      font-weight: 300;
      letter-spacing: -0.02em;
      margin-bottom: 80px;
    }}
    .content {{
      display: flex;
      gap: 120px;
    }}
    .left {{
      flex: 1;
    }}
    .section-label {{
      font-size: 11px;
      font-weight: 500;
      color: #a3a3a3;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 32px;
    }}
    .metrics {{
      display: flex;
      flex-direction: column;
      gap: 0;
    }}
    .metric-row {{
      display: flex;
      justify-content: space-between;
      padding: 24px 0;
      border-bottom: 1px solid #e5e5e5;
    }}
    .metric-label {{
      font-size: 16px;
      color: #737373;
    }}
    .metric-value {{
      font-size: 24px;
      font-weight: 500;
    }}
    .right {{
      flex: 1;
    }}
    .timeline {{
      display: flex;
      flex-direction: column;
      gap: 0;
    }}
    .milestone {{
      padding: 24px 0;
      border-bottom: 1px solid #e5e5e5;
      display: flex;
      gap: 40px;
    }}
    .milestone-date {{
      font-size: 14px;
      color: #a3a3a3;
      width: 80px;
      flex-shrink: 0;
    }}
    .milestone-title {{
      font-size: 16px;
      font-weight: 500;
    }}
    .milestone.done .milestone-title {{
      color: #171717;
    }}
    .milestone.current .milestone-title {{
      font-weight: 600;
    }}
    .milestone.upcoming .milestone-title {{
      color: #a3a3a3;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="content">
    <div class="left">
      <div class="section-label">Metrics</div>
      <div class="metrics">{metrics_html_items}</div>
    </div>
    <div class="right">
      <div class="section-label">Timeline</div>
      <div class="timeline">{timeline_html}</div>
    </div>
  </div>
</body>
</html>'''

        # =====================================================================
        # SALES STYLE - Success-oriented, growth focused
        # =====================================================================
        elif 'sales' in style:
            # Build growth metrics
            growth_cards = ""
            if status_box:
                for item in status_box.get("items", []):
                    change = item.get("change", "")
                    is_positive = "+" in change or "↑" in change
                    growth_cards += f'''
                    <div class="growth-card">
                        <div class="growth-value">{item.get("value", "")}</div>
                        <div class="growth-label">{item.get("label", "")}</div>
                        <div class="growth-change {"up" if is_positive else ""}">{"↑" if is_positive else "↓"} {change}</div>
                    </div>'''

            # Build achievement timeline
            achievements_html = ""
            if milestones:
                for m in milestones:
                    status = m.get("status", "upcoming")
                    icon = "✓" if status == "done" else "●" if status == "current" else "○"
                    achievements_html += f'''
                    <div class="achievement {status}">
                        <div class="achievement-icon">{icon}</div>
                        <div class="achievement-info">
                            <div class="achievement-date">{m.get("date", "")}</div>
                            <div class="achievement-title">{m.get("title", "")}</div>
                        </div>
                    </div>'''

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0c1929;
      color: #ffffff;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
    }}
    .label {{
      font-size: 13px;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }}
    .headline {{
      font-size: 52px;
      font-weight: 800;
      margin-bottom: 50px;
    }}
    .growth-grid {{
      display: flex;
      gap: 24px;
      margin-bottom: 50px;
    }}
    .growth-card {{
      flex: 1;
      background: #132337;
      border-radius: 16px;
      padding: 32px;
      text-align: center;
    }}
    .growth-value {{
      font-size: 48px;
      font-weight: 800;
      color: #10b981;
    }}
    .growth-label {{
      font-size: 16px;
      color: rgba(255,255,255,0.6);
      margin-top: 12px;
    }}
    .growth-change {{
      font-size: 14px;
      font-weight: 600;
      color: rgba(255,255,255,0.4);
      margin-top: 12px;
    }}
    .growth-change.up {{
      color: #10b981;
    }}
    .achievements {{
      display: flex;
      gap: 24px;
    }}
    .achievement {{
      flex: 1;
      background: #132337;
      border-radius: 12px;
      padding: 24px;
      display: flex;
      gap: 16px;
      align-items: flex-start;
      border-left: 4px solid #1e3a5f;
    }}
    .achievement.done {{
      border-left-color: #10b981;
    }}
    .achievement.current {{
      border-left-color: #10b981;
      background: linear-gradient(90deg, rgba(16,185,129,0.1) 0%, #132337 100%);
    }}
    .achievement-icon {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #1e3a5f;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      flex-shrink: 0;
    }}
    .achievement.done .achievement-icon {{
      background: #10b981;
      color: #0c1929;
    }}
    .achievement.current .achievement-icon {{
      background: #10b981;
      color: #0c1929;
      box-shadow: 0 0 0 4px rgba(16,185,129,0.3);
    }}
    .achievement-date {{
      font-size: 12px;
      color: rgba(255,255,255,0.4);
      margin-bottom: 4px;
    }}
    .achievement-title {{
      font-size: 15px;
      font-weight: 600;
    }}
    .achievement.upcoming .achievement-title {{
      color: rgba(255,255,255,0.5);
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="growth-grid">{growth_cards}</div>
  <div class="achievements">{achievements_html}</div>
</body>
</html>'''

        # =====================================================================
        # DEFAULT/TECH STYLE - Modern tech aesthetic
        # =====================================================================
        status_html = ""
        if status_box:
            items_html = ""
            for item in status_box.get("items", []):
                change = item.get("change", "")
                change_color = "#22c55e" if "+" in change or "↑" in change else "#ef4444" if "-" in change or "↓" in change else theme.text_muted
                items_html += f'''
                <div class="status-item">
                    <div class="status-label">{item.get("label", "")}</div>
                    <div class="status-value">{item.get("value", "")}</div>
                    <div class="status-change" style="color: {change_color};">{change}</div>
                </div>
                '''
            status_html = f'''
            <div class="status-box">
                <div class="status-title">{status_box.get("title", "Current Status")}</div>
                <div class="status-items">{items_html}</div>
            </div>
            '''

        milestones_html = ""
        if milestones:
            items_html = ""
            for m in milestones:
                status = m.get("status", "upcoming")
                if status == "done":
                    indicator = f'<div class="milestone-indicator done">✓</div>'
                elif status == "current":
                    indicator = f'<div class="milestone-indicator current"></div>'
                else:
                    indicator = f'<div class="milestone-indicator upcoming"></div>'

                items_html += f'''
                <div class="milestone-item {status}">
                    {indicator}
                    <div class="milestone-content">
                        <div class="milestone-date">{m.get("date", "")}</div>
                        <div class="milestone-title">{m.get("title", "")}</div>
                    </div>
                </div>
                '''
            milestones_html = f'''
            <div class="milestones">
                <div class="milestones-title">Milestones</div>
                <div class="milestones-list">{items_html}</div>
            </div>
            '''

        metrics_html = ""
        if metrics:
            items_html = ""
            for metric in metrics:
                trend = metric.get("trend", "")
                trend_color = "#22c55e" if "+" in trend or "↑" in trend else "#ef4444" if "-" in trend or "↓" in trend else theme.text_muted
                items_html += f'''
                <div class="metric">
                    <div class="metric-value">{metric.get("value", "")}</div>
                    <div class="metric-label">{metric.get("label", "")}</div>
                    <div class="metric-trend" style="color: {trend_color};">{trend}</div>
                </div>
                '''
            metrics_html = f'<div class="metrics">{items_html}</div>'

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Traction</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: {theme.slide_padding};
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 60px;
    }}
    .content-grid {{
      display: flex;
      gap: 60px;
      flex: 1;
    }}
    .status-box {{
      flex: 1;
      background: {theme.surface};
      padding: 40px;
      border-radius: 16px;
    }}
    .status-title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 32px;
    }}
    .status-items {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .status-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 0;
      border-bottom: 1px solid {theme.border};
    }}
    .status-item:last-child {{
      border-bottom: none;
    }}
    .status-label {{
      font-size: 16px;
      color: {theme.text_secondary};
    }}
    .status-value {{
      font-size: 24px;
      font-weight: 700;
    }}
    .status-change {{
      font-size: 14px;
      font-weight: 600;
    }}
    .milestones {{
      flex: 1;
    }}
    .milestones-title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 32px;
    }}
    .milestones-list {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .milestone-item {{
      display: flex;
      gap: 20px;
      align-items: flex-start;
    }}
    .milestone-indicator {{
      width: 24px;
      height: 24px;
      border-radius: 50%;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      color: white;
    }}
    .milestone-indicator.done {{
      background: #22c55e;
    }}
    .milestone-indicator.current {{
      background: {theme.accent};
      box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
    }}
    .milestone-indicator.upcoming {{
      background: {theme.border};
    }}
    .milestone-date {{
      font-size: 14px;
      font-weight: 600;
      color: {theme.text_muted};
      margin-bottom: 4px;
    }}
    .milestone-title {{
      font-size: 18px;
      font-weight: 500;
    }}
    .milestone-item.upcoming .milestone-title {{
      color: {theme.text_muted};
    }}
    .metrics {{
      display: flex;
      gap: 40px;
      margin-top: 48px;
    }}
    .metric {{
      text-align: center;
      flex: 1;
    }}
    .metric-value {{
      font-size: 56px;
      font-weight: 800;
      color: {theme.accent};
    }}
    .metric-label {{
      font-size: 16px;
      color: {theme.text_secondary};
      margin-top: 8px;
    }}
    .metric-trend {{
      font-size: 14px;
      font-weight: 600;
      margin-top: 4px;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  <div class="content-grid">
    {status_html}
    {milestones_html}
  </div>
  {metrics_html}
</body>
</html>'''

    @staticmethod
    def render_demo_slide(
        headline: str,
        label: str = "Product",
        before_content: Optional[Dict[str, Any]] = None,
        after_content: Optional[Dict[str, Any]] = None,
        flow_items: Optional[List[str]] = None,
        screenshot_url: Optional[str] = None,
        theme: Optional[Theme] = None,
    ) -> str:
        """
        Render demo/product slide with style-specific designs.
        Pattern from: runit-pitch/slide-05-demo.html

        before_content: {"title": str, "code": str} or {"title": str, "text": str}
        after_content: {"title": str, "image_url": str} or {"title": str, "text": str}
        flow_items: List of step descriptions
        screenshot_url: Full product screenshot
        """
        theme = theme or LightTheme()
        style = getattr(theme, 'name', 'light')

        # Build content HTML based on mode
        def build_flow_html(style_type: str) -> str:
            if not flow_items:
                return ""
            items_html = ""
            for i, item in enumerate(flow_items):
                items_html += f'''
                <div class="flow-item">
                    <div class="flow-number">{i + 1}</div>
                    <div class="flow-text">{item}</div>
                </div>
                '''
                if i < len(flow_items) - 1:
                    items_html += '<div class="flow-arrow">→</div>'
            return f'<div class="flow-layout">{items_html}</div>'

        # CONSULTING STYLE - Structured, serif accents, numbered steps
        if 'consulting' in style:
            if flow_items:
                items_html = ""
                for i, item in enumerate(flow_items):
                    items_html += f'''
                    <div class="step">
                        <div class="step-number">{i + 1}</div>
                        <div class="step-content">
                            <div class="step-label">Step {i + 1}</div>
                            <div class="step-text">{item}</div>
                        </div>
                    </div>
                    '''
                content_html = f'<div class="steps-layout">{items_html}</div>'
            else:
                content_html = ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Demo</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      display: flex;
      flex-direction: column;
    }}
    .top-bar {{
      height: 6px;
      background: #1a2744;
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
    }}
    .label {{
      font-size: 12px;
      font-weight: 600;
      color: #1a2744;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 24px;
      padding-left: 16px;
      border-left: 3px solid #1a2744;
    }}
    .headline {{
      font-family: {theme.headline_font_family};
      font-size: 52px;
      font-weight: 600;
      line-height: 1.15;
      color: #1a2744;
      margin-bottom: 60px;
    }}
    .steps-layout {{
      display: flex;
      gap: 32px;
      flex: 1;
      align-items: flex-start;
    }}
    .step {{
      flex: 1;
      display: flex;
      gap: 20px;
      padding: 32px;
      background: #f8f9fb;
      border-radius: 4px;
      border-top: 3px solid #1a2744;
    }}
    .step-number {{
      width: 48px;
      height: 48px;
      background: #1a2744;
      color: white;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: 700;
      flex-shrink: 0;
    }}
    .step-content {{
      flex: 1;
    }}
    .step-label {{
      font-size: 12px;
      font-weight: 600;
      color: #6b7c93;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 8px;
    }}
    .step-text {{
      font-size: 18px;
      line-height: 1.6;
      color: #3d5a80;
    }}
  </style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  {content_html}
</body>
</html>'''

        # CONSUMER STYLE - Playful, colorful circles, gradient background
        elif 'consumer' in style:
            if flow_items:
                items_html = ""
                for i, item in enumerate(flow_items):
                    items_html += f'''
                    <div class="flow-item">
                        <div class="flow-circle">{i + 1}</div>
                        <div class="flow-text">{item}</div>
                    </div>
                    '''
                    if i < len(flow_items) - 1:
                        items_html += '<div class="flow-connector"></div>'
                content_html = f'<div class="flow-layout">{items_html}</div>'
            else:
                content_html = ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Demo</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: linear-gradient(180deg, #fffbfc 0%, #fdf2f8 100%);
      color: #1f1f1f;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }}
    .blob {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.4;
    }}
    .blob-1 {{ width: 400px; height: 400px; background: #ec4899; top: -100px; right: -100px; }}
    .blob-2 {{ width: 300px; height: 300px; background: #a855f7; bottom: -50px; left: -50px; }}
    .content {{ position: relative; z-index: 1; flex: 1; display: flex; flex-direction: column; }}
    .label {{
      display: inline-block;
      font-size: 13px;
      font-weight: 700;
      color: #ec4899;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 24px;
      background: rgba(236,72,153,0.1);
      padding: 8px 16px;
      border-radius: 20px;
      width: fit-content;
    }}
    .headline {{
      font-size: 54px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 60px;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .flow-layout {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 24px;
      flex: 1;
    }}
    .flow-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      max-width: 280px;
    }}
    .flow-circle {{
      width: 80px;
      height: 80px;
      background: linear-gradient(135deg, #ec4899, #a855f7);
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      font-weight: 800;
      box-shadow: 0 8px 24px rgba(236,72,153,0.3);
    }}
    .flow-text {{
      text-align: center;
      font-size: 18px;
      color: #4a4a4a;
      background: white;
      padding: 24px;
      border-radius: 24px;
      box-shadow: 0 4px 16px rgba(236,72,153,0.1);
    }}
    .flow-connector {{
      width: 60px;
      height: 4px;
      background: linear-gradient(90deg, #ec4899, #a855f7);
      border-radius: 2px;
    }}
  </style>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="content">
    <div class="label">{label}</div>
    <h1 class="headline">{headline}</h1>
    {content_html}
  </div>
</body>
</html>'''

        # CREATIVE STYLE - Bold, asymmetric, yellow accent sidebar
        elif 'creative' in style:
            if flow_items:
                items_html = ""
                for i, item in enumerate(flow_items):
                    items_html += f'''
                    <div class="flow-card">
                        <div class="card-number">0{i + 1}</div>
                        <div class="card-text">{item}</div>
                    </div>
                    '''
                content_html = f'<div class="flow-grid">{items_html}</div>'
            else:
                content_html = ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Demo</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #0f0f0f;
      color: #ffffff;
      width: 1920px;
      height: 1080px;
      display: flex;
    }}
    .sidebar {{
      width: 120px;
      background: #facc15;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sidebar-text {{
      writing-mode: vertical-rl;
      text-orientation: mixed;
      transform: rotate(180deg);
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: #0f0f0f;
    }}
    .main {{
      flex: 1;
      padding: 80px;
      display: flex;
      flex-direction: column;
    }}
    .headline {{
      font-size: 64px;
      font-weight: 900;
      line-height: 1.0;
      margin-bottom: 60px;
      text-transform: uppercase;
      letter-spacing: -0.03em;
    }}
    .headline span {{
      color: #facc15;
    }}
    .flow-grid {{
      display: flex;
      gap: 32px;
      flex: 1;
      align-items: flex-start;
    }}
    .flow-card {{
      flex: 1;
      background: #1a1a1a;
      padding: 40px;
      border-left: 4px solid #facc15;
    }}
    .card-number {{
      font-size: 48px;
      font-weight: 900;
      color: #facc15;
      margin-bottom: 20px;
    }}
    .card-text {{
      font-size: 20px;
      line-height: 1.6;
      color: rgba(255,255,255,0.8);
    }}
  </style>
</head>
<body>
  <div class="sidebar">
    <span class="sidebar-text">{label}</span>
  </div>
  <div class="main">
    <h1 class="headline">{headline.replace('.', '.<span>*</span>')}</h1>
    {content_html}
  </div>
</body>
</html>'''

        # MINIMAL STYLE - Clean, spacious, subtle
        elif 'minimal' in style:
            if flow_items:
                items_html = ""
                for i, item in enumerate(flow_items):
                    items_html += f'''
                    <div class="step">
                        <div class="step-num">{i + 1}</div>
                        <div class="step-text">{item}</div>
                    </div>
                    '''
                content_html = f'<div class="steps">{items_html}</div>'
            else:
                content_html = ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Demo</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: #fafafa;
      color: #171717;
      width: 1920px;
      height: 1080px;
      padding: 120px 160px;
      display: flex;
      flex-direction: column;
    }}
    .label {{
      font-size: 11px;
      font-weight: 500;
      color: #a3a3a3;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: 48px;
      font-weight: 500;
      line-height: 1.2;
      color: #171717;
      margin-bottom: 80px;
      letter-spacing: -0.02em;
    }}
    .steps {{
      display: flex;
      gap: 80px;
      flex: 1;
    }}
    .step {{
      flex: 1;
      padding-top: 24px;
      border-top: 1px solid #e5e5e5;
    }}
    .step-num {{
      font-size: 14px;
      font-weight: 600;
      color: #a3a3a3;
      margin-bottom: 16px;
    }}
    .step-text {{
      font-size: 18px;
      line-height: 1.8;
      color: #525252;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  {content_html}
</body>
</html>'''

        # SALES STYLE - Dark, emerald accents, compelling
        elif 'sales' in style:
            if flow_items:
                items_html = ""
                for i, item in enumerate(flow_items):
                    items_html += f'''
                    <div class="step-card">
                        <div class="step-badge">Step {i + 1}</div>
                        <div class="step-text">{item}</div>
                    </div>
                    '''
                    if i < len(flow_items) - 1:
                        items_html += '<div class="step-arrow">→</div>'
                content_html = f'<div class="steps-row">{items_html}</div>'
            else:
                content_html = ""

            return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Demo</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.body_font_family};
      background: linear-gradient(180deg, #0c1929 0%, #132337 100%);
      color: #ffffff;
      width: 1920px;
      height: 1080px;
      padding: 80px 100px;
      display: flex;
      flex-direction: column;
    }}
    .label {{
      display: inline-block;
      font-size: 12px;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 24px;
      padding: 8px 16px;
      background: rgba(16,185,129,0.15);
      border-radius: 4px;
      width: fit-content;
    }}
    .headline {{
      font-size: 56px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 60px;
    }}
    .steps-row {{
      display: flex;
      align-items: center;
      gap: 24px;
      flex: 1;
    }}
    .step-card {{
      flex: 1;
      background: rgba(255,255,255,0.05);
      padding: 40px;
      border-radius: 16px;
      border: 1px solid rgba(16,185,129,0.2);
    }}
    .step-badge {{
      display: inline-block;
      font-size: 12px;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      padding: 6px 12px;
      background: rgba(16,185,129,0.15);
      border-radius: 4px;
      margin-bottom: 20px;
    }}
    .step-text {{
      font-size: 20px;
      line-height: 1.6;
      color: rgba(255,255,255,0.9);
    }}
    .step-arrow {{
      font-size: 32px;
      color: #10b981;
      flex-shrink: 0;
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  {content_html}
</body>
</html>'''

        # DEFAULT/TECH STYLE
        if before_content and after_content:
            before_html = ""
            if before_content.get("code"):
                before_html = f'''
                <div class="panel before">
                    <div class="panel-title">{before_content.get("title", "Before")}</div>
                    <pre class="code-block">{before_content.get("code", "")}</pre>
                </div>
                '''
            else:
                before_html = f'''
                <div class="panel before">
                    <div class="panel-title">{before_content.get("title", "Before")}</div>
                    <div class="panel-text">{before_content.get("text", "")}</div>
                </div>
                '''

            after_html = ""
            if after_content.get("image_url"):
                after_html = f'''
                <div class="panel after">
                    <div class="panel-title">{after_content.get("title", "After")}</div>
                    <img src="{after_content.get("image_url")}" class="panel-image" alt="Result">
                </div>
                '''
            else:
                after_html = f'''
                <div class="panel after">
                    <div class="panel-title">{after_content.get("title", "After")}</div>
                    <div class="panel-text">{after_content.get("text", "")}</div>
                </div>
                '''

            content_html = f'''
            <div class="transform-layout">
                {before_html}
                <div class="arrow">→</div>
                {after_html}
            </div>
            '''
        elif flow_items:
            items_html = ""
            for i, item in enumerate(flow_items):
                items_html += f'''
                <div class="flow-item">
                    <div class="flow-number">{i + 1}</div>
                    <div class="flow-text">{item}</div>
                </div>
                '''
                if i < len(flow_items) - 1:
                    items_html += '<div class="flow-arrow">→</div>'
            content_html = f'<div class="flow-layout">{items_html}</div>'
        elif screenshot_url:
            content_html = f'''
            <div class="screenshot-layout">
                <img src="{screenshot_url}" class="screenshot" alt="Product screenshot">
            </div>
            '''
        else:
            content_html = ""

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide - Demo</title>
  <link href="{theme.google_fonts_url}" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {theme.font_family};
      background: {theme.background};
      color: {theme.text_primary};
      width: 1920px;
      height: 1080px;
      padding: {theme.slide_padding};
      display: flex;
      flex-direction: column;
    }}
    .label {{
      font-size: {theme.font_size_label};
      font-weight: {theme.font_weight_semibold};
      color: {theme.text_muted};
      text-transform: uppercase;
      letter-spacing: {theme.letter_spacing_wide};
      margin-bottom: 32px;
    }}
    .headline {{
      font-size: {theme.font_size_headline};
      font-weight: {theme.font_weight_extrabold};
      line-height: {theme.line_height_tight};
      letter-spacing: {theme.letter_spacing_tight};
      margin-bottom: 60px;
    }}
    .transform-layout {{
      display: flex;
      gap: 40px;
      align-items: center;
      flex: 1;
    }}
    .panel {{
      flex: 1;
      background: {theme.surface};
      border-radius: 16px;
      padding: 32px;
      height: 100%;
      display: flex;
      flex-direction: column;
    }}
    .panel-title {{
      font-size: 18px;
      font-weight: 600;
      color: {theme.text_muted};
      margin-bottom: 24px;
    }}
    .code-block {{
      background: #1e1e1e;
      color: #d4d4d4;
      padding: 24px;
      border-radius: 12px;
      font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
      font-size: 14px;
      line-height: 1.6;
      overflow: auto;
      flex: 1;
      white-space: pre-wrap;
    }}
    .panel-text {{
      font-size: 18px;
      line-height: 1.6;
      color: {theme.text_secondary};
    }}
    .panel-image {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 12px;
      flex: 1;
    }}
    .arrow {{
      font-size: 48px;
      color: {theme.accent};
      flex-shrink: 0;
    }}
    .flow-layout {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 24px;
      flex: 1;
    }}
    .flow-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      max-width: 200px;
    }}
    .flow-number {{
      width: 48px;
      height: 48px;
      background: {theme.accent};
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: 700;
    }}
    .flow-text {{
      text-align: center;
      font-size: 16px;
      color: {theme.text_secondary};
    }}
    .flow-arrow {{
      font-size: 32px;
      color: {theme.border};
    }}
    .screenshot-layout {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .screenshot {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }}
  </style>
</head>
<body>
  <div class="label">{label}</div>
  <h1 class="headline">{headline}</h1>
  {content_html}
</body>
</html>'''


class SlideBuilder:
    """Builds complete slide decks from configuration."""

    SLIDE_TYPES = {
        "title": SlideRenderer.render_title_slide,
        "problem": SlideRenderer.render_problem_slide,
        "validation": SlideRenderer.render_validation_slide,
        "solution": SlideRenderer.render_solution_slide,
        "market": SlideRenderer.render_market_slide,
        "comparison": SlideRenderer.render_comparison_slide,
        "funds": SlideRenderer.render_funds_slide,
        "team_ask": SlideRenderer.render_team_ask_slide,
        "content": SlideRenderer.render_content_slide,
        "two_column": SlideRenderer.render_two_column_slide,
        "quote": SlideRenderer.render_quote_slide,
        "numbered_points": SlideRenderer.render_numbered_points_slide,
        "image": SlideRenderer.render_image_slide,
        "pricing": SlideRenderer.render_pricing_slide,
        "traction": SlideRenderer.render_traction_slide,
        "demo": SlideRenderer.render_demo_slide,
    }

    def __init__(self, theme: Optional[Theme] = None):
        self.theme = theme or LightTheme()
        self.slides: List[str] = []

    def add_slide(self, slide_type: str, content: Dict[str, Any]) -> "SlideBuilder":
        """Add a slide to the deck."""
        renderer = self.SLIDE_TYPES.get(slide_type)
        if not renderer:
            raise ValueError(f"Unknown slide type: {slide_type}")

        # Use slide-specific theme if provided, otherwise use builder's theme
        slide_theme = content.pop("theme", None)
        if isinstance(slide_theme, Theme):
            content["theme"] = slide_theme
        elif slide_theme == "dark":
            content["theme"] = DarkTheme()
        elif slide_theme == "light":
            content["theme"] = LightTheme()
        else:
            content["theme"] = self.theme

        try:
            html = renderer(**content)
        except (TypeError, AttributeError, KeyError) as e:
            # Fallback: render as simple content slide if the specific renderer fails
            headline = content.get("headline", slide_type.replace("_", " ").title())
            theme = content.get("theme", self.theme)
            html = SlideRenderer.render_content_slide(
                headline=headline,
                content_html=f"<p>{content.get('subheadline', '')}</p>",
                label=content.get("label", slide_type.replace("_", " ").title()),
                theme=theme,
            )
        self.slides.append(html)
        return self

    def build(self) -> List[str]:
        """Build all slides and return HTML strings."""
        return self.slides

    # Style-to-theme mapping
    STYLE_THEMES = {
        "tech": {"dark": PitchDarkTheme, "light": PitchLightTheme},
        "saas": {"dark": PitchDarkTheme, "light": PitchLightTheme},
        "consulting": {"dark": ConsultingDarkTheme, "light": ConsultingLightTheme},
        "consumer": {"dark": ConsumerDarkTheme, "light": ConsumerLightTheme},
        "creative": {"dark": CreativeDarkTheme, "light": CreativeLightTheme},
        "agency": {"dark": CreativeDarkTheme, "light": CreativeLightTheme},
        "minimal": {"dark": MinimalDarkTheme, "light": MinimalLightTheme},
        "sales": {"dark": SalesDarkTheme, "light": SalesLightTheme},
    }

    def build_from_config(self, config: Dict[str, Any]) -> List[str]:
        """
        Build deck from JSON config.

        Config structure:
        {
            "style": "consulting",  # Style preset: tech, consulting, consumer, creative, minimal, sales
            "theme": {...},  # Optional theme overrides
            "slides": [
                {"type": "title", "content": {...}},
                {"type": "problem", "content": {...}},
                ...
            ]
        }
        """
        # Get style preset (determines color scheme)
        style = config.get("style", "tech")
        style_themes = self.STYLE_THEMES.get(style, self.STYLE_THEMES["tech"])

        # Only override theme if not already set externally (e.g., from DeckGenerator.render())
        if not hasattr(self, '_theme_externally_set') or not self._theme_externally_set:
            if "theme" in config:
                theme_config = config["theme"]
                if theme_config.get("mode") == "dark":
                    self.theme = style_themes["dark"]()
                else:
                    self.theme = style_themes["light"]()
                for key, value in theme_config.items():
                    if hasattr(self.theme, key):
                        setattr(self.theme, key, value)
            else:
                self.theme = style_themes["light"]()

        # Store style themes for per-slide theme handling
        self._style_themes = style_themes

        # Generate each slide
        for slide_config in config.get("slides", []):
            slide_type = slide_config["type"]
            content = slide_config.get("content", {}).copy()

            # Handle per-slide theme, preserving custom fonts from base theme
            if "theme" in slide_config:
                slide_theme = slide_config["theme"]
                if slide_theme == "dark":
                    t = self._style_themes["dark"]()
                elif slide_theme == "light":
                    t = self._style_themes["light"]()
                else:
                    t = slide_theme
                # Preserve font settings from the externally-set theme
                if isinstance(t, Theme) and hasattr(self.theme, 'headline_font_family'):
                    t.headline_font_family = self.theme.headline_font_family
                    t.body_font_family = self.theme.body_font_family
                    if hasattr(self.theme, 'mono_font_family'):
                        t.mono_font_family = self.theme.mono_font_family
                content["theme"] = t

            self.add_slide(slide_type, content)

        return self.build()


# Module-level alias for SLIDE_TYPES
SLIDE_TYPES = SlideBuilder.SLIDE_TYPES
