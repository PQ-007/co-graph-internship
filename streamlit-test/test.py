from streamlit_elements import elements, html
import base64

def display_gif_icon_direct(gif_path_or_url, size=24):
    with elements("gif_icon_container"):
        gif_src = ""
        if gif_path_or_url.startswith("http"):
            gif_src = gif_path_or_url
        else:
            try:
                with open(gif_path_or_url, "rb") as file:
                    contents = file.read()
                    gif_src = f"data:image/gif;base64,{base64.b64encode(contents).decode('utf-8')}"
            except FileNotFoundError:
                html.div("Animated icon file not found.")
                return

        html.img(
            src=gif_src,
            style={
                "width": f"{size}px",
                "height": f"{size}px",
                "verticalAlign": "middle", # Helps align with text if used inline
                # Add any other CSS for icon-like styling (e.g., margin)
            }
        )

# Example usage:
# Assuming you have a local 'loading_icon.gif' file
# display_gif_icon_direct("loading_icon.gif", size=32)

# Using a URL for an animated icon
display_gif_icon_direct("https://media.giphy.com/media/l0HlC6Mko639P0RjW/giphy.gif", size=48)