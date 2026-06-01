from pathlib import Path
from image import fetch_image_local, fetch_image_web, image_to_string
from image_source import ImageSource


class PrintLayer:
    def __init__(
        self,
        layer_error: str,
        layer_number: int,
        layer_height: float,
        material_type: str,
        extrusion_temperature: int,
        print_speed: int,
        layer_adhesion_quality: str,
        infill_density: int,
        infill_pattern: str,
        shell_thickness: int,
        overhang_angle: int,
        cooling_fan_speed: int,
        retraction_settings: str,
        z_offset_adjustment: float,
        print_bed_temperature: int,
        layer_time: str,
        file_name: str,
        image_url: str,
        image_data: str,
    ):
        self._layer_error = layer_error
        self._layer_number = layer_number
        self._layer_height = layer_height
        self._material_type = material_type
        self._extrusion_temperature = extrusion_temperature
        self._print_speed = print_speed
        self._layer_adhesion_quality = layer_adhesion_quality
        self._infill_density = infill_density
        self._infill_pattern = infill_pattern
        self._shell_thickness = shell_thickness
        self._overhang_angle = overhang_angle
        self._cooling_fan_speed = cooling_fan_speed
        self._retraction_settings = retraction_settings
        self._z_offset_adjustment = z_offset_adjustment
        self._print_bed_temperature = print_bed_temperature
        self._layer_time = layer_time
        self._file_name = file_name
        self._image_url = image_url
        self._image_data = image_data

    @classmethod
    def from_csv_row(cls, row: list[str], image_source: ImageSource) -> 'PrintLayer':
        """Construct a PrintLayer instance from a fixed-order CSV row."""
        file_name = row[16].strip()
        image_url = row[17].strip()

        # retrieve the image data
        if image_source == ImageSource.LOCAL:
            local_file_name = Path(file_name).with_suffix(".tiff").name
            image_data = fetch_image_local("images", local_file_name)
        else:
            image_data = fetch_image_web(image_url)
        
        # convert image data to a string so it can be stored in the output file
        if image_data is not None:
            image_data_str = image_to_string(image_data)
        else:
            image_data_str = ""

        return cls(
            layer_error=row[0].strip(),
            layer_number=int(row[1].strip()),
            layer_height=float(row[2].strip()),
            material_type=row[3].strip(),
            extrusion_temperature=int(row[4].strip()),
            print_speed=int(row[5].strip()),
            layer_adhesion_quality=row[6].strip(),
            infill_density=int(row[7].strip()),
            infill_pattern=row[8].strip(),
            shell_thickness=int(row[9].strip()),
            overhang_angle=int(row[10].strip()),
            cooling_fan_speed=int(row[11].strip()),
            retraction_settings=row[12].strip(),
            z_offset_adjustment=float(row[13].strip()),
            print_bed_temperature=int(row[14].strip()),
            layer_time=row[15].strip(),
            file_name=file_name,
            image_url=image_url,
            image_data=image_data_str,
        )

    def to_jsonl(self):
        import json
        return json.dumps({
            "layer_error": self._layer_error,
            "layer_number": self._layer_number,
            "layer_height": self._layer_height,
            "material_type": self._material_type,
            "extrusion_temperature": self._extrusion_temperature,
            "print_speed": self._print_speed,
            "layer_adhesion_quality": self._layer_adhesion_quality,
            "infill_density": self._infill_density,
            "infill_pattern": self._infill_pattern,
            "shell_thickness": self._shell_thickness,
            "overhang_angle": self._overhang_angle,
            "cooling_fan_speed": self._cooling_fan_speed,
            "retraction_settings": self._retraction_settings,
            "z_offset_adjustment": self._z_offset_adjustment,
            "print_bed_temperature": self._print_bed_temperature,
            "layer_time": self._layer_time,
            "file_name": self._file_name,
            "image_url": self._image_url,
            "image_data": self._image_data
        })

    @property
    def layer_error(self) -> str:
        return self._layer_error
    @layer_error.setter
    def layer_error(self, value: str) -> None:
        self._layer_error = value

    @property
    def layer_number(self) -> int:
        return self._layer_number
    @layer_number.setter
    def layer_number(self, value: int) -> None:
        self._layer_number = value

    @property
    def layer_height(self) -> float:
        return self._layer_height
    @layer_height.setter
    def layer_height(self, value: float) -> None:
        self._layer_height = value

    @property
    def material_type(self) -> str:
        return self._material_type
    @material_type.setter
    def material_type(self, value: str) -> None:
        self._material_type = value

    @property
    def extrusion_temperature(self) -> int:
        return self._extrusion_temperature
    @extrusion_temperature.setter
    def extrusion_temperature(self, value: int) -> None:
        self._extrusion_temperature = value

    @property
    def print_speed(self) -> int:
        return self._print_speed
    @print_speed.setter
    def print_speed(self, value: int) -> None:
        self._print_speed = value

    @property
    def layer_adhesion_quality(self) -> str:
        return self._layer_adhesion_quality
    @layer_adhesion_quality.setter
    def layer_adhesion_quality(self, value: str) -> None:
        self._layer_adhesion_quality = value

    @property
    def infill_density(self) -> int:
        return self._infill_density
    @infill_density.setter
    def infill_density(self, value: int) -> None:
        self._infill_density = value

    @property
    def infill_pattern(self) -> str:
        return self._infill_pattern
    @infill_pattern.setter
    def infill_pattern(self, value: str) -> None:
        self._infill_pattern = value

    @property
    def shell_thickness(self) -> int:
        return self._shell_thickness
    @shell_thickness.setter
    def shell_thickness(self, value: int) -> None:
        self._shell_thickness = value

    @property
    def overhang_angle(self) -> int:
        return self._overhang_angle
    @overhang_angle.setter
    def overhang_angle(self, value: int) -> None:
        self._overhang_angle = value

    @property
    def cooling_fan_speed(self) -> int:
        return self._cooling_fan_speed
    @cooling_fan_speed.setter
    def cooling_fan_speed(self, value: int) -> None:
        self._cooling_fan_speed = value

    @property
    def retraction_settings(self) -> str:
        return self._retraction_settings
    @retraction_settings.setter
    def retraction_settings(self, value: str) -> None:
        self._retraction_settings = value

    @property
    def z_offset_adjustment(self) -> float:
        return self._z_offset_adjustment
    @z_offset_adjustment.setter
    def z_offset_adjustment(self, value: float) -> None:
        self._z_offset_adjustment = value

    @property
    def print_bed_temperature(self) -> int:
        return self._print_bed_temperature
    @print_bed_temperature.setter
    def print_bed_temperature(self, value: int) -> None:
        self._print_bed_temperature = value

    @property
    def layer_time(self) -> str:
        return self._layer_time
    @layer_time.setter
    def layer_time(self, value: str) -> None:
        self._layer_time = value

    @property
    def file_name(self) -> str:
        return self._file_name
    @file_name.setter
    def file_name(self, value: str) -> None:
        self._file_name = value

    @property
    def image_url(self) -> str:
        return self._image_url
    @image_url.setter
    def image_url(self, value: str) -> None:
        self._image_url = value

    @property
    def image_data(self) -> str:
        return self._image_data
    @image_data.setter
    def image_data(self, value: str) -> None:
        self._image_data = value
