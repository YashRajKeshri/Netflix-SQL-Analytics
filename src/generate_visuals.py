"""
Netflix SQL Analytics - Visual Asset Generator
Generates clean, modern SVG charts for documentation and README reporting based on 25,000 records.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = PROJECT_ROOT / "docs" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def generate_tier_distribution_svg():
    """Generates subscription tier breakdown chart."""
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 350" width="100%" height="100%">
  <defs>
    <linearGradient id="premGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E50914"/>
      <stop offset="100%" stop-color="#B20710"/>
    </linearGradient>
    <linearGradient id="stdGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#4A90E2"/>
      <stop offset="100%" stop-color="#2D68C4"/>
    </linearGradient>
    <linearGradient id="basicGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F5A623"/>
      <stop offset="100%" stop-color="#D98200"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#141414" rx="12"/>
  <text x="30" y="45" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Subscription Tier & Revenue Distribution (25,000 Users)</text>
  <text x="30" y="70" fill="#AAAAAA" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13">Monthly Recurring Revenue (MRR: $404,307/mo) & Subscriber Proportions</text>
  
  <!-- Premium -->
  <text x="30" y="120" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="14" font-weight="600">Premium Tier ($22.99/mo)</text>
  <text x="610" y="120" fill="#E50914" font-family="-apple-system, sans-serif" font-size="14" font-weight="700">47.8% MRR</text>
  <rect x="30" y="132" width="640" height="24" rx="6" fill="#222222"/>
  <rect x="30" y="132" width="306" height="24" rx="6" fill="url(#premGrad)"/>
  <text x="40" y="149" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">8,402 Subscribers (33.6%) • $193,161.98 MRR</text>

  <!-- Standard -->
  <text x="30" y="195" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="14" font-weight="600">Standard Tier ($15.49/mo)</text>
  <text x="610" y="195" fill="#4A90E2" font-family="-apple-system, sans-serif" font-size="14" font-weight="700">31.6% MRR</text>
  <rect x="30" y="207" width="640" height="24" rx="6" fill="#222222"/>
  <rect x="30" y="207" width="202" height="24" rx="6" fill="url(#stdGrad)"/>
  <text x="40" y="224" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">8,242 Subscribers (33.0%) • $127,668.58 MRR</text>

  <!-- Basic -->
  <text x="30" y="270" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="14" font-weight="600">Basic Tier ($9.99/mo)</text>
  <text x="610" y="270" fill="#F5A623" font-family="-apple-system, sans-serif" font-size="14" font-weight="700">20.6% MRR</text>
  <rect x="30" y="282" width="640" height="24" rx="6" fill="#222222"/>
  <rect x="30" y="282" width="132" height="24" rx="6" fill="url(#basicGrad)"/>
  <text x="40" y="299" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">8,356 Subscribers (33.4%) • $83,476.44 MRR</text>
</svg>
"""
    output_path = IMAGES_DIR / "tier_distribution.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✓ Generated: {output_path}")


def generate_country_ranking_svg():
    """Generates regional performance ranking chart."""
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 380" width="100%" height="100%">
  <defs>
    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E50914"/>
      <stop offset="100%" stop-color="#FF5A5F"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#141414" rx="12"/>
  <text x="30" y="45" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Top Regional Markets by Aggregate Streamed Hours</text>
  <text x="30" y="70" fill="#AAAAAA" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13">Aggregated Streamed Hours (Total: 12.5M+ Hours Across 25,000 Users)</text>

  <!-- Germany -->
  <text x="30" y="115" fill="#EEEEEE" font-family="-apple-system, sans-serif" font-size="13" font-weight="600">Germany (2,547 users)</text>
  <rect x="180" y="100" width="420" height="20" rx="4" fill="#222222"/>
  <rect x="180" y="100" width="420" height="20" rx="4" fill="url(#barGrad)"/>
  <text x="610" y="115" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">1.26M hrs</text>

  <!-- Brazil -->
  <text x="30" y="155" fill="#EEEEEE" font-family="-apple-system, sans-serif" font-size="13" font-weight="600">Brazil (2,503 users)</text>
  <rect x="180" y="140" width="420" height="20" rx="4" fill="#222222"/>
  <rect x="180" y="140" width="420" height="20" rx="4" fill="url(#barGrad)"/>
  <text x="610" y="155" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">1.26M hrs</text>

  <!-- USA -->
  <text x="30" y="195" fill="#EEEEEE" font-family="-apple-system, sans-serif" font-size="13" font-weight="600">USA (2,520 users)</text>
  <rect x="180" y="180" width="420" height="20" rx="4" fill="#222222"/>
  <rect x="180" y="180" width="418" height="20" rx="4" fill="url(#barGrad)"/>
  <text x="610" y="195" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">1.25M hrs</text>

  <!-- France -->
  <text x="30" y="235" fill="#EEEEEE" font-family="-apple-system, sans-serif" font-size="13" font-weight="600">France (2,520 users)</text>
  <rect x="180" y="220" width="420" height="20" rx="4" fill="#222222"/>
  <rect x="180" y="220" width="417" height="20" rx="4" fill="url(#barGrad)"/>
  <text x="610" y="235" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">1.25M hrs</text>

  <!-- Australia -->
  <text x="30" y="275" fill="#EEEEEE" font-family="-apple-system, sans-serif" font-size="13" font-weight="600">Australia (2,488 users)</text>
  <rect x="180" y="260" width="420" height="20" rx="4" fill="#222222"/>
  <rect x="180" y="260" width="413" height="20" rx="4" fill="url(#barGrad)"/>
  <text x="610" y="275" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">1.24M hrs</text>

  <!-- Canada -->
  <text x="30" y="315" fill="#EEEEEE" font-family="-apple-system, sans-serif" font-size="13" font-weight="600">Canada (2,510 users)</text>
  <rect x="180" y="300" width="420" height="20" rx="4" fill="#222222"/>
  <rect x="180" y="300" width="412" height="20" rx="4" fill="url(#barGrad)"/>
  <text x="610" y="315" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">1.24M hrs</text>

  <!-- UK -->
  <text x="30" y="355" fill="#EEEEEE" font-family="-apple-system, sans-serif" font-size="13" font-weight="600">UK (2,456 users)</text>
  <rect x="180" y="340" width="420" height="20" rx="4" fill="#222222"/>
  <rect x="180" y="340" width="411" height="20" rx="4" fill="url(#barGrad)"/>
  <text x="610" y="355" fill="#FFFFFF" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">1.23M hrs</text>
</svg>
"""
    output_path = IMAGES_DIR / "country_ranking.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✓ Generated: {output_path}")


if __name__ == "__main__":
    generate_tier_distribution_svg()
    generate_country_ranking_svg()
    print("🎨 All visual assets regenerated successfully!")
