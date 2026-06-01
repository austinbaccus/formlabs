# fakeprinter

## design

### requirements:
- Can run on this computer as well as a Raspberry Pi CM4 
    - Those can have as little as 1GB of RAM, and a good chunk of that is going to be used for OS overhead
- Implied ARM compatibility
- 2M slices per print

### inputs
- print name
- output folder
- mode selection (supervised or automatic)

### runtime
- read in CSV of fake print data laysers
- in supervised mode:
    - when user presses "return" output a fake print layer to the file system (filesystem design is up to me, but must contain all data)
    - provide immediate user feedback on any errors that occur in the data set
    - user can ignore error or end fakeprint job when an error pops up
- in automatic mode:
    - should run fully even if errors occur

### outputs
- at the end of a fakeprint job:
    - provide summary to user
    - can be any format, be creative!