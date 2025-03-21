from rich.prompt import Prompt
import os
from pathlib import Path
import platformdirs
import json

def make_language_choice() -> str:
    """Interactive language selection with persistence."""
    config_path = Path(platformdirs.user_config_dir("llm-code-ctx")) / "config.json"
    
    # Try to load saved preferences
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                prefs = json.load(f)
                if "language" in prefs:
                    if Prompt.ask(
                        f"⚙️  Use saved language preference [cyan]({prefs['language']})[/]?", 
                        choices=["y", "n"], 
                        default="y"
                    ) == "y":
                        return prefs['language']
        except Exception as e:
            pass
            
    # Interactive selection
    lang = Prompt.ask(
        "🔠 Choose language to analyze",
        choices=["py", "js", "ts", "java", "go"],
        default="py"
    )
    
    # Save preference
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump({"language": lang}, f)
    except Exception as e:
        pass
        
