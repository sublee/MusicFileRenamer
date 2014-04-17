from distutils.core import setup
import py2exe

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>myProgram</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
""" 

setup(name="Music Manager",
        windows=[{
            "script": "app.py",
            "icon_resources": [(1, "images\\pill.ico")],
            "other_resources": [(24,1,manifest)]
        }],
        data_files=[("images", ["images\\add.png",
                                "images\\cd.png",
                                "images\\disk.png",
                                "images\\disk_multiple.png",
                                "images\\folder.png",
                                "images\\information.png",
                                "images\\music.png",
                                "images\\page_white.png",
                                "images\\pill.png",
                                "images\\tag_blue.png",
                                "images\\user.png",
                                "images\\world_go.png",
                                "images\\wrench_orange.png"])])

# python setup.py py2exe --includes encodings --packages encodings
