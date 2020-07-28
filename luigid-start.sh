#!/bin/sh
cat << "EOF"
 _____       __    __    _____      _____     _____
(_   _)      ) )  ( (   (_   _)    / ___ \   (_   _)
  | |       ( (    ) )    | |     / /   \_)    | |
  | |        ) )  ( (     | |    ( (  ____     | |
  | |   __  ( (    ) )    | |    ( ( (__  )    | |
__| |___) )  ) \__/ (    _| |__   \ \__/ /    _| |__
\________/   \______/   /_____(    \____/    /_____(
EOF
echo "Luigi: $(python -c 'import luigi; print(luigi.__meta__.__version__)')"
echo "$(python -VV)"

# Note that this .sh is modified to include any command line args passed in to
# pass through to luigid

# Make sure to chmod +x this file
exec luigid $@