from firebase.database.reference import get_style_ref


def add_style_name(style_name):
    print("add_style_name/Push value=%s" % style_name)
    get_style_ref().child(style_name).set(style_name)


def refresh_style_names(style_names):
    clone_style_names = style_names.copy()
    ref = get_style_ref()
    previous_styles = ref.get()
    previous_styles_iter = previous_styles.each()
    if previous_styles_iter is None:
        for style_name in clone_style_names:
            add_style_name(style_name)
    else:
        for style in previous_styles_iter:
            key = style.item[0]
            value = style.item[1]

            if value in clone_style_names:
                print("refresh_style_names/Remove value=%s" % value)
                clone_style_names.remove(value)

        for style_name in clone_style_names:
            add_style_name(style_name)


def cleaning_root():
    from firebase.database.reference import get_root
    db = get_root()
    rootitems = db.get()
    rootitems_iter = rootitems.each()
    if rootitems_iter is not None:
        for each in rootitems_iter:
            key = each.item[0]
            value = each.item[1]
            print("cleaning_root/each item value type = %s" % type(value))
            if type(value) is str:
                print("cleaning_root/each item key = %s, value = %s" % (key, value))
                db.child(key).remove()
