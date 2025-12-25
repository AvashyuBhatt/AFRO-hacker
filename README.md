# Pokemon Fire Red Binary Hacking Tool

A comprehensive ROM hacking tool for Pokemon Fire Red with advanced features including roaming Pokemon mechanics, alpha Pokemon system, and quest management. The interface is designed to be identical to Hex Maniac Advance while providing powerful new functionality.

## Features

### Core Functionality
- **ROM Loading and Editing**: Load and modify Pokemon Fire Red ROM files with full binary editing capabilities
- **Hex Maniac Advance Interface**: Familiar interface design for existing ROM hackers
- **Symbol File Integration**: Utilizes pokefirered.sym for accurate asset location mapping
- **Drag-and-Drop Sprite Management**: Intuitive sprite placement and map editing

### Advanced Features
- **Roaming Pokemon System**: Create Pokemon that move around the game world and can chase or interact with the player
- **Alpha Pokemon Mechanics**: Enhanced Pokemon with increased size, special effects, and boosted stats
- **Quest System**: Comprehensive quest management with visual indicators and reward systems
- **Map Editor**: Full map editing capabilities with layer management and asset organization

## Installation

### Requirements
- Python 3.11 or higher
- Windows operating system (for final executable)

### Setup
1. Clone or download the project
2. Navigate to the project directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
cd src
python main.py
```

### Loading a ROM
1. Open the application
2. Go to File > Open ROM...
3. Select your Pokemon Fire Red ROM file
4. The application will validate and load the ROM

### Using Features

#### Roaming Pokemon
1. Navigate to View > Roaming Pokemon
2. Select Pokemon to enable roaming behavior
3. Configure behavior settings (aggressive/passive/mixed)
4. Set movement speed and chase range
5. Apply changes to ROM

#### Alpha Pokemon
1. Navigate to View > Alpha Pokemon
2. Select Pokemon to make Alpha variants
3. Adjust size multiplier, level boost, and stat multipliers
4. Configure glow effects and aggression levels
5. Add custom movesets if desired

#### Quest System
1. Navigate to View > Quest System
2. Create new quests with objectives and rewards
3. Place quest markers on the map
4. Configure quest logic and completion conditions

#### Map Editing
1. Navigate to View > Map Editor
2. Select location from dropdown menu
3. Drag sprites from palette to map
4. Use layer controls to manage different map elements
5. Save changes to ROM

## Project Structure

```
pokemon_fire_red_hacker/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── core/              # Core ROM manipulation
│   ├── ui/                # User interface modules
│   ├── features/          # Feature implementations
│   └── utils/             # Utility functions
├── assets/                # Application assets
├── docs/                  # Documentation
├── tests/                 # Unit tests
├── build/                 # Build artifacts
└── requirements.txt       # Python dependencies
```

## Building Executable

To create a Windows executable:

```bash
pyinstaller --onefile --windowed --name "Pokemon Fire Red Hacker" src/main.py
```

The executable will be created in the `dist/` directory.

## Contributing

This project is designed to be a comprehensive ROM hacking tool. Contributions are welcome for:
- Bug fixes and improvements
- Additional Pokemon game support
- New features and enhancements
- Documentation improvements

## License

This project is for educational and personal use only. Pokemon Fire Red is a trademark of Nintendo/Game Freak/Creatures Inc.

## Acknowledgments

- Hex Maniac Advance for interface design inspiration
- pret/pokefirered decompilation project for symbol file
- Pokemon ROM hacking community for tools and techniques
                                                           Enjoy!-ThatOneGreen (creator)



                                                               