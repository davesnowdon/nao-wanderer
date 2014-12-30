<?xml version="1.0" encoding="UTF-8" ?>
<Package name="wanderer" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="." xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs />
    <Resources>
        <File name="defaults_en" src="resources/defaults_en.properties" />
        <File name="wanderer" src="resources/wanderer.json" />
        <File name="quit" src="resources/sounds/quit.wav" />
        <File name="index" src="resources/web/index.html" />
        <File name="jquery-1.9.1.min" src="resources/web/jquery-1.9.1.min.js" />
        <File name="__init__" src="src/main/python/naoutil/__init__.py" />
        <File name="avahi" src="src/main/python/naoutil/avahi.py" />
        <File name="broker" src="src/main/python/naoutil/broker.py" />
        <File name="general" src="src/main/python/naoutil/general.py" />
        <File name="i18n" src="src/main/python/naoutil/i18n.py" />
        <File name="jprops" src="src/main/python/naoutil/jprops.py" />
        <File name="jsonobj" src="src/main/python/naoutil/jsonobj.py" />
        <File name="memory" src="src/main/python/naoutil/memory.py" />
        <File name="naoenv" src="src/main/python/naoutil/naoenv.py" />
        <File name="README" src="src/main/python/naoutil/README" />
        <File name="__init__" src="src/main/python/util/__init__.py" />
        <File name="__init__" src="src/main/python/util/__init__.pyc" />
        <File name="geometry" src="src/main/python/util/geometry.py" />
        <File name="httputil" src="src/main/python/util/httputil.py" />
        <File name="mathutil" src="src/main/python/util/mathutil.py" />
        <File name="mathutil" src="src/main/python/util/mathutil.pyc" />
        <File name="__init__" src="src/main/python/wanderer/__init__.py" />
        <File name="action" src="src/main/python/wanderer/action.py" />
        <File name="dataposter" src="src/main/python/wanderer/dataposter.py" />
        <File name="event" src="src/main/python/wanderer/event.py" />
        <File name="grid" src="src/main/python/wanderer/grid.py" />
        <File name="grid_mapper" src="src/main/python/wanderer/grid_mapper.py" />
        <File name="http" src="src/main/python/wanderer/http.py" />
        <File name="randomwalk" src="src/main/python/wanderer/randomwalk.py" />
        <File name="robotstate" src="src/main/python/wanderer/robotstate.py" />
        <File name="wanderer" src="src/main/python/wanderer/wanderer.py" />
        <File name="__init__" src="src/test/python/data_collector/__init__.py" />
        <File name="client" src="src/test/python/data_collector/client.py" />
        <File name="main" src="src/test/python/data_collector/main.py" />
        <File name="__init__" src="src/test/python/naoutil_tests/__init__.py" />
        <File name="README" src="src/test/python/naoutil_tests/README" />
        <File name="__init__" src="src/test/python/wanderer_tests/__init__.py" />
        <File name="mock" src="src/test/python/wanderer_tests/mock.py" />
        <File name="run_httpd" src="src/test/python/wanderer_tests/run_httpd.py" />
        <File name="run_pygame" src="src/test/python/wanderer_tests/run_pygame.py" />
        <File name="test_action" src="src/test/python/wanderer_tests/test_action.py" />
        <File name="test_eventhandlers" src="src/test/python/wanderer_tests/test_eventhandlers.py" />
        <File name="test_events" src="src/test/python/wanderer_tests/test_events.py" />
        <File name="test_executor" src="src/test/python/wanderer_tests/test_executor.py" />
        <File name="test_geometry" src="src/test/python/wanderer_tests/test_geometry.py" />
        <File name="test_grid" src="src/test/python/wanderer_tests/test_grid.py" />
        <File name="test_obstacle_direction" src="src/test/python/wanderer_tests/test_obstacle_direction.py" />
        <File name="test_wanderer" src="src/test/python/wanderer_tests/test_wanderer.py" />
    </Resources>
    <Topics />
    <IgnoredPaths />
</Package>
