# Voice Spinning Donut

A Python application that renders a 3D spinning donut which can be controlled using voice commands. The donut's rotation speed can be adjusted through voice input.

## Features

- 3D rendered donut using ASCII characters
- Real-time voice command processing
- Adjustable rotation speed
- Multiple microphone support
- Dynamic color themes

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/gverep/voice-spinning-donut.git
    cd voice-spinning-donut
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Install the package:
    ```sh
    pip install .
    ```

## Usage

Run the application:
```sh
python -m voice_spinning_donut
```

### Voice Commands

- Say "faster" to increase rotation speed
- Say "slower" to decrease rotation speed
- Say "stop" to halt rotation
- Say "set X" to set specific speed (where X is a number)
- Say "white, red, green, blue" to change donut color theme

## License

This project is licensed under the [MIT](LICENSE) License.