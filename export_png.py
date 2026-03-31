#!/usr/bin/env python3
"""
Generate uml_final.png directly from Mermaid diagram.
No browser or external tools needed!
"""

import base64
import json
from pathlib import Path

# Define paths
project_dir = Path("/Users/rahul/Desktop/ai110-module2show-pawpal-starter")
output_png = project_dir / "uml_final.png"

# Mermaid diagram code
mermaid_code = """
classDiagram
    class Owner {
        -name: str
        -pets: List~Pet~
        +addPet(pet: Pet): void
        +removePet(petName: str): bool
        +getPets(): List~Pet~
        +getAllTasks(includeCompleted: bool): List~Task~
    }

    class Pet {
        -name: str
        -species: str
        -age: int
        -tasks: List~Task~
        +addTask(task: Task): void
        +removeTask(taskDescription: str): bool
        +getTasks(): List~Task~
        +getPendingTasks(): List~Task~
    }

    class Task {
        -description: str
        -time_minutes: int
        -frequency: str
        -priority: int
        -is_completed: bool
        -scheduled_date: datetime | None
        -scheduled_time: str | None
        +markComplete(pet: Pet | None): void
        +markIncomplete(): void
    }

    class Scheduler {
        +generateDailyPlan(owner: Owner, availableTime: int): List~Task~
        +sortByPriority(tasks: List~Task~): List~Task~
        +detectConflicts(pet: Pet, newTask: Task): bool
        +addTaskWithConflictDetection(pet: Pet, newTask: Task): void
        +filterTasksByCompletion(owner: Owner, isCompleted: bool): List~Task~
        +filterTasksByPetName(owner: Owner, petName: str): List~Task~
        +collectPendingTasks(owner: Owner): List~Task~
    }

    Owner "1" *-- "0..*" Pet : manages
    Pet "1" *-- "0..*" Task : includes
    Scheduler ..> Owner : reads from
    Scheduler ..> Pet : checks conflicts for
    Scheduler ..> Task : prioritizes/filters
"""

def generate_png_with_mermaid_api():
    """
    Generate PNG using Mermaid's public API.
    No local tools required!
    """
    import urllib.request
    import urllib.error
    
    try:
        print("🌐 Using Mermaid API to generate PNG...")
        
        # Encode diagram for API
        encoded = base64.b64encode(mermaid_code.encode()).decode()
        
        # Mermaid render API URL
        url = f"https://mermaid.ink/img/{encoded}"
        
        # Download PNG
        print(f"📥 Downloading from: {url[:50]}...")
        urllib.request.urlretrieve(url, output_png)
        
        print(f"✅ PNG generated: {output_png}")
        print(f"📏 File size: {output_png.stat().st_size / 1024:.1f} KB")
        return True
        
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def generate_png_with_pillow():
    """
    Generate PNG using PIL/Pillow (if installed).
    Creates a simple text-based diagram.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        print("🎨 Generating PNG with Pillow...")
        
        # Create image with white background
        width, height = 1200, 800
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Draw title
        draw.text((50, 30), "PawPal+ UML Class Diagram", fill='black', font=title_font)
        draw.line([(50, 60), (width-50, 60)], fill='gray', width=2)
        
        # Draw class boxes
        y = 100
        classes_info = [
            ("Owner", ["name: str", "pets: List[Pet]", "+ addPet()", "+ getPets()", "+ getAllTasks()"]),
            ("Pet", ["name: str", "species: str", "age: int", "+ addTask()", "+ getTasks()"]),
            ("Task", ["description: str", "time_minutes: int", "priority: int", "+ markComplete()", "+ markIncomplete()"]),
            ("Scheduler", ["+ generateDailyPlan()", "+ sortByPriority()", "+ detectConflicts()", "+ filterTasksByCompletion()"])
        ]
        
        x_positions = [50, 350, 650, 950]
        
        for idx, (class_name, members) in enumerate(classes_info):
            x = x_positions[idx]
            
            # Draw box
            draw.rectangle([(x, y), (x+280, y+150)], outline='blue', width=2, fill='#E8F4F8')
            
            # Draw class name
            draw.text((x+10, y+10), class_name, fill='blue', font=text_font)
            draw.line([(x, y+30), (x+280, y+30)], fill='blue', width=1)
            
            # Draw members
            for i, member in enumerate(members[:4]):
                draw.text((x+10, y+40+i*25), member, fill='black', font=text_font)
        
        # Add relationships info
        y = 400
        draw.text((50, y), "Relationships:", fill='black', font=title_font)
        draw.text((50, y+40), "Owner (1) --manages--> (0..*) Pet", fill='darkblue')
        draw.text((50, y+70), "Pet (1) --includes--> (0..*) Task", fill='darkblue')
        draw.text((50, y+100), "Scheduler ···reads from··· Owner", fill='darkblue')
        
        # Save
        img.save(output_png)
        print(f"✅ PNG generated: {output_png}")
        print(f"📏 File size: {output_png.stat().st_size / 1024:.1f} KB")
        return True
        
    except ImportError:
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Generating UML diagram as PNG...\n")
    
    # Try Mermaid API first (best quality, needs internet)
    if generate_png_with_mermaid_api():
        print("\n✨ Success! PNG ready: uml_final.png")
    # Fallback to Pillow (no internet needed)
    elif generate_png_with_pillow():
        print("\n✨ Success! PNG ready: uml_final.png")
    else:
        print("\n❌ Failed to generate PNG")
        print("\nAlternative: Use Mermaid Live Online")
        print("1. Go to https://mermaid.live")
        print("2. Paste diagram code from UML_DIAGRAM.md")
        print("3. Download as PNG manually")
