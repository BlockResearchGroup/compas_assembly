********************************************************************************
Getting Started
********************************************************************************

.. highlight:: bash


Requirements
============

* `Anaconda <https://www.anaconda.com/download>`_
* `Github <https://github.com>`_ account
* `Git <https://git-scm.com/downloads>`_


Installation
============

In this tutorial, we will create a new virtual environment with ``conda`` to install
``compas_assembly``. We will name the environment ``assembly``, but you can use any
name you like.

If you wish to install ``compas_assembly`` in an already existing environment, just
skip the first step and simply activate the environment of your choice.


1. Create a virtual environment and install COMPAS
--------------------------------------------------

* https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments

::

    $ conda create -n assembly -c conda-forge python=3.6 COMPAS


2. Activate the environment
---------------------------

* https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments


**On Mac**

::

    $ source activate assembly


**On Windows**

::

    $ activate assembly


3. Install dependencies
-----------------------

* https://shapely.readthedocs.io/en/latest/


**On Mac**

::

    pip install shapely[vectorized]


**On Windows**

::

    conda install -n assembly -c conda-forge shapely


4. Fork package
---------------

* `COMPAS assembly <https://github.com/BlockResearchGroup/compas_assembly>`_


Go to https://github.com/BlockResearchGroup/compas_assembly and *fork* the repository to your
personal account. This will simplify the development process when you will start
making changes to the code or when you want to start contributing.


5. Clone forked package
-----------------------

* https://github.com/<your-username>/compas_assembly

Clone the forked package to a location on your computer.

::

    $ mkdir ~/Code/COMPAS-packages
    $ cd ~/Code/COMPAS-packages
    $ git clone https://github.com/<your-username>/compas_assembly.git


6. Install cloned package
-------------------------

::

    $ cd compas_assembly
    $ pip install -r requirements-dev.txt


7. Check installation
---------------------

Start an interactive Python session in the Terminal.

>>> import compas
>>> import compas_assembly


8. Install packages for Rhino
-----------------------------

**On Mac**

::

    $ python -m compas_rhinomac.install compas compas_rhino compas_assembly


**On Windows**

*Not available yet.*


9. Install Rhino plugin
-----------------------

**On Mac**

*Not available yet.*


**On Windows**

*Not available yet.*

