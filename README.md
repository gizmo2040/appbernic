# Appbernic Framework README

## Introduction

Hello! I'm gizmo2040, and I'd like to introduce you to **Appbernic**, a framework for creating applications for Anbernic devices using Python and Pillow. This project is based on some amazing initial work by **macc-n**, who developed the code for handling input and rendering graphics with Pillow. I took that as a foundation and built a framework around it, expanding its potential to create more structured and feature-rich applications.

### Purpose

The appbernic framework allows developers to easily create and manage apps that can be deployed on Anbernic devices running Ubuntu. The goal is to simplify the development process while giving people the power to build cool, innovative apps that enhance their experience with these handheld consoles.

## Features

- **Modular Framework**: Inspired by tools like React, you can generate apps independently using the framework.
- **Pillow Rendering**: Graphics are rendered using the Pillow library.
- **Input Handling**: Input system allows user interactions with the console. 
- **Theming**: I created a **Matrix theme**, inspired by the cyberpunk aesthetic of the movie *The Matrix*, which had a big influence on me growing up.
  
## Installation

To install the appbernic framework, simply clone the repository and follow the setup instructions:

```bash
cd AppName/lib/
git clone https://github.com/yourusername/appbernic.git
```

You’ll also may need to install Pillow, which handles all the rendering work for images.

## How to Use

Once you’ve set up the framework, you can generate new applications. The directory structure is as follows:

```
/AppName/
    ├── assets/
    ├── src/
        ├── lib/
            ├── appbernic/
        ├── main.py
        ├── app.py
    ├── README.md
    └── AppName.sh
```

Each app has its own assets, source files, and build scripts to make the deployment process simple.

### Key Features

- **Modular Components**: Apps created are independent of the framework and can be customized further.
- **Graphics**: All graphics-related functions are handled by `appbernic.graphics.py`.
- **Input**: Handling inputs and navigation ( needs to be updated to non blocking ).

### Example

```python
from lib.appbernic import graphic as gr, input

def main():
    gr.draw_text((100, 50), "Hello, appbernic!")
    while True:
        input.check()
        if input.key("A"):
            gr.draw_log("Button A Pressed")

if __name__ == "__main__":
    main()
```

## The Philosophy Behind appbernic

My work on *Appbernic* is deeply inspired by the [GNU movement](https://www.youtube.com/watch?v=NrI-0u4npGo) and Richard Stallman’s vision. The idea that software should serve people and empower them to understand, modify, and share it has always resonated with me. Just like the characters in The Matrix who took the Red Pill and challenged the true nature of reality, Stallman questioned the restrictive nature of locked-down software. This framework is one way for me to contribute to that vision of making free software —not in terms of price, but in terms of freedom.

I believe in the freedom to use, change, and distribute software without boundaries. It’s a tool meant to do good, much like Stallman’s ideals for free software and open collaboration. This project stands as a testament to those who seek to look beyond the given constraints and create something new for the benefit of all, pushing back against limitations and promoting freedom in technology.

## License

This project is licensed under the GNU General Public License (GPL). This license, much like the ideals of Richard Stallman and the GNU movement, allows for free use, modification, and sharing of the software. If you're curious about the philosophy behind this movement, I encourage you to take the “red pill,” follow the white rabbit, and explore how deep the rabbit hole of [open-source software](https://www.youtube.com/watch?v=jw8K460vx1c) goes.

---

Feel free to contribute, file issues, and share your apps created with appbernic. Let's build something amazing together!