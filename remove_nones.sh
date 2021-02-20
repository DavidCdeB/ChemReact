#

# This is to parse the below tex file, so that it correctly compiles the table of reactions where Max.dis/Min.dist >= 1.1
file="Reactions_Closed_Table_more_than_1_1.tex"
filetmp="tmp.tex"
newfile="Reactions_Closed_Table_more_than_1_1_ready.tex"

# If there is a reaction where all events are "none"
# throw away lines that contain this block:
# \multirow
# \multirow
# \hline
pcregrep  -v -M "multirow.*\n.*multirow.*\n.*hline"  ${file}  > ${filetmp}

# here we save the line numbers that contain \cline{3-8} when \cline{3-8} is followed by \hline:
lines=$(pcregrep   -M -n "cline{3-8}.*\n.*hline" ${filetmp}  | awk '{print $1}' | grep -v "^\\\\" | sed  's/:.*//')
# don't need to do the complicated way:
#lines=$(pcregrep   -M -n "cline{3-8}.*\n.*hline" *1_1.tex  | awk '{print $1}' | grep -v "^\\\\" | sed  -e 's|:.*||' | xargs)

# command to delete these lines at once:
if [ -z "${lines}" ]
then
      echo "lines are empty"
else
    echo "lines are NOT empty"
    cmd=`echo ${lines} | sed 's/ /d;/g' | sed 's/$/d/g'`
    sed -i.bak "${cmd}" ${filetmp}
fi
cp ${filetmp} ${newfile}

# Now you need to fix the number of rows for each reaction,
# and replace that number in the \multirow{here}
