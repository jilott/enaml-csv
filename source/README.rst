THis is a preliminary look at the CSV editor.

Find the repository at:
http://www.github.com/jaidevd/enaml-csv

**Description of the UI**

    .. image:: https://raw.github.com/jaidevd/enaml-csv/master/source/viz_widgets/Icons/screenshot.png

Clone the repository and cd into the /source/CsvModel directory. Then run the
editor_launch.py file. At first sight, you should be able to see a UI with a table
on the left and a set of tabbed regions on the right. The table on the left initially
contains zeros. Use the 'Load' button below the table to load any csv file. There is
one sample file, 'sample.csv' in the /datasets folder.

On the right of the UI you should see four tabs on the top, the first of which has
four nested tabs. In the following part of the document we shall take a look
at the more interesting functions of the editor, classified into these tabbed regions.

*1. Data Visualization*
------------------------------------------------------------------------------
Basic data visualization widgets are nested under this tab, of which the X-Y plots
have the most features.

1.1 X-Y Plotting
``````````````````````````````````````````````````````````````````````````````
Initially, the XY plotting tab shows an empty region with a set of controls to
its right. When a file is loaded into the table view on the left, selections from
the table can be used to generate and XY plots to the plotting canvas.

Since XY plotting can work only on two arrays of equal length, only selecting
two columns or two rows will work here. Select any two columns from the table
view by clicking one column and then another holding down the ctrl key. Now
select properties of the plot from the menu on the right. Clicking the 'Color'
field brings up a standard color picker (default is blue). Select the type of plot
between discrete and continuous (default is continuous). You can add a name to the
plot in the 'Plot Name' field. If no name is supplied, a default name will be used.
Clicking 'Plot from Selection' will draw this plot, and it will be added to the
list of plots, seen below the 'Plot From Selection' button. You can go on adding
plots by selecting pairs of columns from the table, each with it's own properties.
Zooming and panning works on these plots. TraitsTool works with limited functionality.

CAUTION: Muptiple plots will create multiple tick intervals and grids.

Plots can also be removed from the canvas by selecting them from the list and
clicking the 'Remove Selected Plots' button.

TODO:
Add Legend,
Improve TraitsTool,
Saving plots to images.
Some items are TraitsUI items, find out how to make a colorpicker in enaml.


1.2 Image Plots
``````````````````````````````````````````````````````````````````````````````

Any selection created by dragging a box around contiguous cells can be used to
create image plots. Drag a selection around any region in the table an click the
'Use Selection Button'

TODO:
Add chaco tools,
Add Colorbar.

1.3 Principal Component Plots
```````````````````````````````````````````````````````````````````````````````

These plots are used for a 2-D representation of higher dimensional data. The
dimensionality reduction is done using PCA. PCA based dimensionality reduction
can be performed on any 2-D array like data. Create such a selection through the
table view and click 'Use Selection' to see the plots.

TODO:
Add chaco tools,
Plots should be editable.

*2. Data Analysis*
------------------------------------------------------------------------------

This tab (currently) shows statistics of the current selection. Make any selection
in the table view (not necessarily contiguous) and click 'Use Selection' to see the
sum, mean, variance, etc of the selection.

TODO:
All the numerically intensive applications should go here. Could add curve fitting,
parameter estimation, etc

*3. Other*
------------------------------------------------------------------------------

raise NotImplementedError

TODO:
Sorting rows and columns is easy, but those actions should be undoable.


*4. Scripting*
-----------------------------------------------------------------------------
Type an arbitrary python script in the text editor and click 'Run'. The script
executes and the generated variables are all listed in the view to the right of the
text editor, alongwith the properties of all variables (name, type, dimensions,
size in bytes)

Making a selection and clicking 'Use Selection' shows a pop-up with the list of
the selections. The user should be able to name these selections and use them as variables
in the script. Eg. if I select a row, click 'Use Selection' and call that row 'x',
then typing 'print x' in the editor should work.

TODO:
Add selections to the workspace.
















