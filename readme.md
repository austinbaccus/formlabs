# FakePrint

This is a Formlabs take-home test.

## How To Run

```
git clone https://github.com/austinbaccus/formlabs.git
cd formlabs
```

### Linux & Raspberry Pi
```
python3 src/main.py --print-name "formlabs_test" --output-folder ./output --mode "supervised" --image-source "cloud"
```

### Windows
```
python src\main.py --print-name "formlabs_test" --output-folder ./output --mode "automatic" --image-source "local"
```

### Supported Platforms
| Platform | Supported |
|----------|-----------|
| Windows (64-bit) | ✅ |
| Linux (64-bit) | ✅ |
| Raspberry Pi (ARM) | ✅ |

# Design Considerations

## Multi-platform Support
I added support for Windows, but I also want this to work on Linux. Specifically, I want this to work with Raspberry Pi machines, since they were mentioned in the instructions. 

With that in mind, I did get this running on my Windows 11 machine, Ubuntu machine, and Raspberry Pi 4. I've added more details (including screenshots) in the `misc` folder. 

## Condensed image data in output file
The original format for each print layer image is 8-bit depth PNG. This results in a typical file size of around 9KB. I wanted to include the image data in the output file, so making each image as small as possible was my goal. I implemented two changes to make this happen:

1. Changed bit-depth to 1 instead of 8
2. Converted all images to `.TIFF`

This reduces each image file size from 9KB to ~1-2KB.

`TIFF` had a smaller file size than `PNG` in my testing, which is why I chose it over `PNG`. I chose 1-bit pixel depth because I noticed all images were black and white with no greyscale... so why not go with 1-bit color depth to save file space?

## Support for reading images from local or cloud storage

I added support for fetching images locally or from the Google Drive provided by the spec. The reason I added a local option was because it was a pain to sit for ~3 minutes to retrieve all the images.

This can be selected via the CLI arguments:
```
 --image-source "cloud"
 --image-source "local"
```
