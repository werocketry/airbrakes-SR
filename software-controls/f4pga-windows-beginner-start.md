# Getting F4PGA

This section describes how to install F4PGA and set up a fully working environment to later build example designs on Windows.

## Prerequisites

To be able to follow through this tutorial, install the following software:

First, ensure you have Git installed. You can download it from [Git for Windows](https://gitforwindows.org/). Additionally, install a package manager for Windows like Chocolatey from [Chocolatey](https://chocolatey.org/install).

Using Chocolatey, install wget and xz-utils:

```bash
choco install wget
choco install xz-utils
```

Next, clone the F4PGA examples repository and enter it:

```bash
git clone https://github.com/chipsalliance/f4pga-examples
cd f4pga-examples
```

## Toolchain installation

Now we are able to install the F4PGA toolchain. This procedure is divided into three steps:

1. Installing the Conda package manager,
2. Choosing an installation directory,
3. Downloading the architecture definitions and installing the toolchain.

### Conda

Download Conda installer script into the `f4pga-examples` directory:

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe -O conda_installer.exe
```

### Choose the install directory

The install directory can either be in your user directory such as `C:\Users\YourUsername\opt\f4pga` or in a system directory such as `C:\opt\f4pga`. If you choose a system directory, you will need administrator permission to perform the installation.

```bash
set F4PGA_INSTALL_DIR=C:\Users\YourUsername\opt\f4pga
```

### Setup and download assets

Select your target FPGA family:

```bash
set FPGA_FAM=eos-s3
```

Next, setup Conda and your system’s environment, and download architecture definitions:

```bash
start /wait "" conda_installer.exe /InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=%F4PGA_INSTALL_DIR%\%FPGA_FAM%\conda
call "%F4PGA_INSTALL_DIR%\%FPGA_FAM%\conda\Scripts\activate.bat"
conda env create -f %FPGA_FAM%\environment.yml
```

```bash
set F4PGA_PACKAGES='install-ql ql-eos-s3_wlcsp'

mkdir %F4PGA_INSTALL_DIR%\%FPGA_FAM%

set F4PGA_TIMESTAMP='20220920-124259'
set F4PGA_HASH='007d1c1'

for %%i in (%F4PGA_PACKAGES%) do (
  wget -qO- https://storage.googleapis.com/symbiflow-arch-defs/artifacts/prod/foss-fpga-tools/symbiflow-arch-defs/continuous/install/%F4PGA_TIMESTAMP%/symbiflow-arch-defs-%%i-%F4PGA_HASH%.tar.xz | tar -xJ -C %F4PGA_INSTALL_DIR%\%FPGA_FAM%
)
```

If the above commands exited without errors, you have successfully installed and configured your working environment.

**Important**

With the toolchain installed, you are ready to build the example designs! Examples are provided in separated directories:

- Subdir `xc7` for the Artix-7 devices
- Subdir `eos-s3` for the EOS S3 devices

**Hint**

Sometimes it may be preferable to get the latest versions of the tools before the pinned versions in this repository are updated. Latest versions are not guaranteed to be bug-free, but they enable users to take advantage of fixes. See Bumping/overriding specific tools.
