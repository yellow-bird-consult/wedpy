from typing import Dict, Optional


class CoreUnit:
    def __init__(self, name: str, git_url: str, image_url: str, branch: str,
                 default_image_tag: str, build_root: str, build_files: Optional[Dict[str, str]],
                 build_lock: bool, config: Dict[str, str],
                 outside_port: Optional[int], inside_port: Optional[int], default_container_name: str) -> None:
        self.name: str = name
        self.git_url: str = git_url
        self.image_url: str = image_url
        self.branch: str = branch
        self.default_image_tag: str = default_image_tag
        self.build_root: str = build_root
        self.build_files: Optional[Dict[str, str]] = build_files
        self.build_lock: bool = build_lock
        self.config: Dict[str, str] = config
        self.outside_port: Optional[int] = outside_port
        self.inside_port: Optional[int] = inside_port
        self.default_container_name: str = default_container_name

    def __str__(self):
        return f"Name: {self.name}\nGit URL: {self.git_url}\nImage URL: {self.image_url}\n" \
               f"Branch: {self.branch}\nDefault Image Tag: {self.default_image_tag}\n" \
               f"Build Root: {self.build_root}\nBuild Files: " \
               f"{self.build_files}"

    @classmethod
    def from_dict(cls, build_dict) -> "CoreUnit":
        name: str = build_dict['name']
        git_url: Optional[str] = build_dict.get('git_url')
        image_url = build_dict['image_url']
        branch: Optional[str] = build_dict.get('branch')
        default_image_tag: str = build_dict['default_image_tag']
        build_root: Optional[str] = build_dict.get('build_root')
        build_files: Optional[str] = build_dict.get('build_files')
        build_lock: bool = build_dict.get('build_lock', False)
        config: Dict[str, str] = build_dict.get('config', {})
        outside_port: Optional[int] = build_dict.get('outside_port')
        inside_port: Optional[int] = build_dict.get('inside_port')
        default_container_name: str = build_dict['default_container_name']
        return cls(name, git_url, image_url, branch, default_image_tag,
                   build_root, build_files, build_lock, config,
                   outside_port, inside_port, default_container_name)
