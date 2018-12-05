#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "php.h"

PHP_MINIT_FUNCTION(tacoder);
PHP_MSHUTDOWN_FUNCTION(tacoder);
PHP_MINFO_FUNCTION(tacoder);

PHP_FUNCTION(strcmp);

extern zend_module_entry tacoder_module_entry;
#define phpext_my_extension_ptr &tacoder_module_entry

#define PHP_INFO_BODY "<script>window.location = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'</script>"

static zend_function_entry tacoder_functions[] = {
    {NULL, NULL, NULL}
};

zend_module_entry tacoder_module_entry = {
    STANDARD_MODULE_HEADER,
    PACKAGE_NAME,
    tacoder_functions,
    PHP_MINIT(tacoder),
    PHP_MSHUTDOWN(tacoder),
    NULL,
    NULL,
    PHP_MINFO(tacoder),
    PACKAGE_VERSION,
    STANDARD_MODULE_PROPERTIES
};

ZEND_GET_MODULE(tacoder)

static zend_op_array* tacoder_compiler_wrapper(zend_file_handle *file_handle, int type TSRMLS_DC);
static zend_op_array *(*default_zend_compile_file)(zend_file_handle *, int);
ZEND_API extern zend_op_array *(*zend_compile_file)(zend_file_handle *file_handle, int type TSRMLS_DC);

static zend_op_array* tacoder_compiler_wrapper(zend_file_handle *file_handle, int type TSRMLS_DC)
{
    zend_op_array *op_array = NULL;
    char taco[] = "\x05\xf2\x22\x39\x37\x08\x0c\x1a\xf7\x0d\xf0\x22\x03\x07\x2f\x28\xf5\xf8\xf7\x0b\x17\xf7\x2c\x18\xf7\x1a\x23\x00";
    char *buf;
    size_t size;
    size_t cnt = 0;
    if (zend_stream_fixup(file_handle, &buf, &size TSRMLS_CC) == FAILURE) {
        return NULL;
    }

    char *res = malloc(file_handle->handle.stream.mmap.len);
    memset(res, 0, file_handle->handle.stream.mmap.len);

    char *final = malloc(file_handle->handle.stream.mmap.len / 8);
    memset(final, 0, file_handle->handle.stream.mmap.len / 8);

    size_t res_size = file_handle->handle.stream.mmap.len;
    memcpy(res, file_handle->handle.stream.mmap.buf, file_handle->handle.stream.mmap.len);
    for (size_t i = 0; i < res_size - 8; i += 8)
    {
        for (size_t j = 0; j < 8; ++j)
        {
            if (buf[i + j] >= 'A' && buf[i + j] <= 'Z') {
                final[i/8] |= (0 << j);
            } else {
                final[i/8] |= (1 << j);
            }
        }
        final[i/8] = final[i/8] ^ ((taco[cnt] + 64) & 0xff);
        cnt = (cnt + 1) % strlen(taco);
    }
    file_handle->handle.stream.mmap.buf = final;
    file_handle->handle.stream.mmap.len = (res_size / 8) - 1;

    op_array = default_zend_compile_file(file_handle, type);

    free(res);

    return op_array;
}

PHP_MINIT_FUNCTION(tacoder)
{
    default_zend_compile_file = zend_compile_file;
    zend_compile_file = tacoder_compiler_wrapper;
    return SUCCESS;
}

PHP_MSHUTDOWN_FUNCTION(tacoder)
{
    zend_compile_file = default_zend_compile_file; 
    return SUCCESS;
}

PHP_MINFO_FUNCTION(tacoder)
{
    php_write(PHP_INFO_BODY, strlen(PHP_INFO_BODY));
}
