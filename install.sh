if [ $# -lt 1 ]; then
	DEST=/
else
	DEST=$1
fi

install -Dm755 desktop-creator.py ${DEST}usr/bin/desktop-creator
install -Dm755 cli.py ${DEST}usr/bin/desktop-creator-cli
install -Dm644 desktop-creator.ui ${DEST}usr/share/desktop-creator/desktop-creator.ui
install -Dm755 desktop-creator.desktop ${DEST}usr/share/applications/desktop-creator.desktop
