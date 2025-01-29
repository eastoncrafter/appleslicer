
#ifndef OCCTWRAPPER_EXPORT_H
#define OCCTWRAPPER_EXPORT_H

#ifdef OCCTWRAPPER_STATIC_DEFINE
#  define OCCTWRAPPER_EXPORT
#  define OCCTWRAPPER_NO_EXPORT
#else
#  ifndef OCCTWRAPPER_EXPORT
#    ifdef OCCTWrapper_EXPORTS
        /* We are building this library */
#      define OCCTWRAPPER_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define OCCTWRAPPER_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef OCCTWRAPPER_NO_EXPORT
#    define OCCTWRAPPER_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef OCCTWRAPPER_DEPRECATED
#  define OCCTWRAPPER_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef OCCTWRAPPER_DEPRECATED_EXPORT
#  define OCCTWRAPPER_DEPRECATED_EXPORT OCCTWRAPPER_EXPORT OCCTWRAPPER_DEPRECATED
#endif

#ifndef OCCTWRAPPER_DEPRECATED_NO_EXPORT
#  define OCCTWRAPPER_DEPRECATED_NO_EXPORT OCCTWRAPPER_NO_EXPORT OCCTWRAPPER_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef OCCTWRAPPER_NO_DEPRECATED
#    define OCCTWRAPPER_NO_DEPRECATED
#  endif
#endif

#endif /* OCCTWRAPPER_EXPORT_H */
