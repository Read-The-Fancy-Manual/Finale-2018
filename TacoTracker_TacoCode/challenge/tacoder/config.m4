PHP_ARG_ENABLE(tacoder, whether to enable tacoder support,
[ --enable-tacoder   Enable tacoder support])

if test "$PHP_TACODER" = "yes"; then
    AC_DEFINE(HAVE_TACODER, 1, [Whether you have tacoder])
    PHP_NEW_EXTENSION(tacoder, tacoder.c, $ext_shared)
fi
