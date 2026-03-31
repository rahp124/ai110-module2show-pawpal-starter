#!/usr/bin/env python3
"""
Generate UML diagram PNG by creating SVG and converting locally.
Works offline without external APIs.
"""

from pathlib import Path

project_dir = Path("/Users/rahul/Desktop/ai110-module2show-pawpal-starter")

# Create SVG version of the diagram
svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900">
  <!-- Background -->
  <rect width="1400" height="900" fill="white"/>
  
  <!-- Title -->
  <text x="700" y="40" font-size="32" font-weight="bold" text-anchor="middle" fill="#333">
    PawPal+ UML Class Diagram - Final Implementation
  </text>
  
  <!-- Owner Class -->
  <g>
    <rect x="50" y="100" width="280" height="220" fill="#E8F4F8" stroke="#0066CC" stroke-width="2" rx="5"/>
    <text x="190" y="130" font-size="18" font-weight="bold" text-anchor="middle" fill="#0066CC">Owner</text>
    <line x1="50" y1="145" x2="330" y2="145" stroke="#0066CC" stroke-width="1"/>
    <text x="60" y="165" font-size="12" fill="#333">- name: str</text>
    <text x="60" y="185" font-size="12" fill="#333">- pets: List[Pet]</text>
    <line x1="50" y1="200" x2="330" y2="200" stroke="#0066CC" stroke-width="1"/>
    <text x="60" y="220" font-size="12" fill="#0066CC">+ addPet(pet: Pet)</text>
    <text x="60" y="240" font-size="12" fill="#0066CC">+ removePet(name: str)</text>
    <text x="60" y="260" font-size="12" fill="#0066CC">+ getPets()</text>
    <text x="60" y="280" font-size="12" fill="#0066CC">+ getAllTasks()</text>
    <text x="60" y="300" font-size="12" fill="#0066CC">+ getAll() → List[Task]</text>
  </g>
  
  <!-- Pet Class -->
  <g>
    <rect x="420" y="100" width="280" height="220" fill="#E8F4F8" stroke="#0066CC" stroke-width="2" rx="5"/>
    <text x="560" y="130" font-size="18" font-weight="bold" text-anchor="middle" fill="#0066CC">Pet</text>
    <line x1="420" y1="145" x2="700" y2="145" stroke="#0066CC" stroke-width="1"/>
    <text x="430" y="165" font-size="12" fill="#333">- name: str</text>
    <text x="430" y="185" font-size="12" fill="#333">- species: str</text>
    <text x="430" y="205" font-size="12" fill="#333">- age: int</text>
    <text x="430" y="225" font-size="12" fill="#333">- tasks: List[Task]</text>
    <line x1="420" y1="240" x2="700" y2="240" stroke="#0066CC" stroke-width="1"/>
    <text x="430" y="260" font-size="12" fill="#0066CC">+ addTask(task: Task)</text>
    <text x="430" y="280" font-size="12" fill="#0066CC">+ removeTask(desc: str)</text>
    <text x="430" y="300" font-size="12" fill="#0066CC">+ getTasks()</text>
  </g>
  
  <!-- Task Class -->
  <g>
    <rect x="790" y="100" width="280" height="260" fill="#E8F4F8" stroke="#0066CC" stroke-width="2" rx="5"/>
    <text x="930" y="130" font-size="18" font-weight="bold" text-anchor="middle" fill="#0066CC">Task</text>
    <line x1="790" y1="145" x2="1070" y2="145" stroke="#0066CC" stroke-width="1"/>
    <text x="800" y="165" font-size="11" fill="#333">- description: str</text>
    <text x="800" y="183" font-size="11" fill="#333">- time_minutes: int</text>
    <text x="800" y="201" font-size="11" fill="#333">- frequency: str</text>
    <text x="800" y="219" font-size="11" fill="#333">- priority: int</text>
    <text x="800" y="237" font-size="11" fill="#333">- is_completed: bool</text>
    <text x="800" y="255" font-size="11" fill="#333">- scheduled_time: str</text>
    <line x1="790" y1="270" x2="1070" y2="270" stroke="#0066CC" stroke-width="1"/>
    <text x="800" y="290" font-size="11" fill="#0066CC">+ markComplete()</text>
    <text x="800" y="308" font-size="11" fill="#0066CC">+ markIncomplete()</text>
  </g>
  
  <!-- Scheduler Class -->
  <g>
    <rect x="1100" y="100" width="280" height="260" fill="#E8F4F8" stroke="#0066CC" stroke-width="2" rx="5"/>
    <text x="1240" y="130" font-size="18" font-weight="bold" text-anchor="middle" fill="#0066CC">Scheduler</text>
    <line x1="1100" y1="145" x2="1380" y2="145" stroke="#0066CC" stroke-width="1"/>
    <line x1="1100" y1="150" x2="1380" y2="150" stroke="#CCCCCC" stroke-width="1"/>
    <text x="1110" y="170" font-size="10" fill="#0066CC">+ generateDailyPlan()</text>
    <text x="1110" y="187" font-size="10" fill="#0066CC">+ sortByPriority()</text>
    <text x="1110" y="204" font-size="10" fill="#0066CC">+ detectConflicts()</text>
    <text x="1110" y="221" font-size="10" fill="#0066CC">+ addTask...Conflict()</text>
    <text x="1110" y="238" font-size="10" fill="#0066CC">+ filterByCompletion()</text>
    <text x="1110" y="255" font-size="10" fill="#0066CC">+ filterByPetName()</text>
    <text x="1110" y="272" font-size="10" fill="#0066CC">+ collectPendingTasks()</text>
  </g>
  
  <!-- Relationships -->
  <!-- Owner to Pet (composition) -->
  <line x1="330" y1="210" x2="420" y2="210" stroke="#333" stroke-width="2"/>
  <polygon points="420,210 410,205 410,215" fill="#333"/>
  <text x="370" y="200" font-size="11" fill="#333">manages (1..*)</text>
  
  <!-- Pet to Task (composition) -->
  <line x1="700" y1="210" x2="790" y2="210" stroke="#333" stroke-width="2"/>
  <polygon points="790,210 780,205 780,215" fill="#333"/>
  <text x="740" y="200" font-size="11" fill="#333">includes (1..*)</text>
  
  <!-- Scheduler dependencies (dashed lines) -->
  <!-- To Owner -->
  <line x1="1100" y1="230" x2="330" y2="230" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="700" y="250" font-size="10" fill="#666" text-anchor="middle">reads from</text>
  
  <!-- To Pet -->
  <line x1="1100" y1="250" x2="700" y2="320" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="850" y="295" font-size="10" fill="#666">checks conflicts for</text>
  
  <!-- To Task -->
  <line x1="1100" y1="270" x2="1070" y2="270" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="1085" y="290" font-size="10" fill="#666">prioritizes/filters</text>
  
  <!-- Legend -->
  <g>
    <rect x="50" y="550" width="1300" height="300" fill="#F5F5F5" stroke="#CCCCCC" stroke-width="1" rx="5"/>
    <text x="70" y="580" font-size="16" font-weight="bold" fill="#333">📋 Implementation Details</text>
    
    <text x="70" y="610" font-size="13" font-weight="bold" fill="#0066CC">Key Features:</text>
    <text x="70" y="630" font-size="12" fill="#333">✅ Task Scheduling: Time (HH:MM), Date, Recurring (daily/weekly)</text>
    <text x="70" y="650" font-size="12" fill="#333">✅ Conflict Detection: Identifies time-based scheduling conflicts</text>
    <text x="70" y="670" font-size="12" fill="#333">✅ Multi-level Filtering: By pet, completion status, priority, available time</text>
    <text x="70" y="690" font-size="12" fill="#333">✅ Auto-recurring: markComplete() creates next occurrence if frequency set</text>
    
    <text x="700" y="610" font-size="13" font-weight="bold" fill="#0066CC">Scheduler Methods (7 total):</text>
    <text x="700" y="630" font-size="12" fill="#333">• generateDailyPlan() - Fits tasks into available time</text>
    <text x="700" y="650" font-size="12" fill="#333">• sortByPriority() - Prioritizes by importance &amp; duration</text>
    <text x="700" y="670" font-size="12" fill="#333">• detectConflicts() - Checks for scheduling conflicts</text>
    <text x="700" y="690" font-size="12" fill="#333">• filterTasksByCompletion/PetName/Time() - Multi-level filtering</text>
  </g>
  
  <!-- Footer -->
  <text x="700" y="880" font-size="11" fill="#999" text-anchor="middle">
    PawPal+ Pet Care Planning System | Final Implementation | March 31, 2026
  </text>
</svg>
'''

# Save as SVG
svg_file = project_dir / "uml_diagram.svg"
svg_file.write_text(svg_content)
print(f"✅ SVG created: {svg_file}")

# Now try to convert SVG to PNG
try:
    # Try using cairosvg if available
    import cairosvg
    png_file = project_dir / "uml_final.png"
    cairosvg.svg2png(bytestring=svg_content.encode(), write_to=str(png_file))
    print(f"✅ PNG created with cairosvg: {png_file}")
except ImportError:
    print("⚠️  cairosvg not available, trying alternative method...")
    
    try:
        # Try using svglib + PIL
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        
        drawing = svg2rlg(str(svg_file))
        renderPM.drawToFile(drawing, str(project_dir / "uml_final.png"), fmt="PNG")
        print(f"✅ PNG created with reportlab: {project_dir / 'uml_final.png'}")
    except ImportError:
        print("⚠️  reportlab not available")
        print("\n📋 Alternative: Use the SVG file directly")
        print(f"   SVG file: {svg_file}")
        print("\n   Or open uml_final.html in browser and click 'Download as PNG'")
except Exception as e:
    print(f"❌ Error converting SVG: {e}")
