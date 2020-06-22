.. code-block:: bash 
    
    # get orders, with authorization, wrong user
    curl http://localhost:5000/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:2"
    
..

.. code-block:: json 

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
      "http://www.w3.org/TR/html4/loose.dtd">
    <html>
      <head>
        <title>AttributeError: 'OrderCollection' object has no attribute 'order_by' // Werkzeug Debugger</title>
        <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css"
            type="text/css">
        <!-- We need to make sure this has a favicon so that the debugger does
             not by accident trigger a request to /favicon.ico which might
             change the application state. -->
        <link rel="shortcut icon"
            href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
        <script src="?__debugger__=yes&amp;cmd=resource&amp;f=jquery.js"></script>
        <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
        <script type="text/javascript">
          var TRACEBACK = 139756087320400,
              CONSOLE_MODE = false,
              EVALEX = true,
              EVALEX_TRUSTED = false,
              SECRET = "bhWwxgdCMJiqXpJAdUty";
        </script>
      </head>
      <body style="background-color: #fff">
        <div class="debugger">
    <h1>AttributeError</h1>
    <div class="detail">
      <p class="errormsg">AttributeError: 'OrderCollection' object has no attribute 'order_by'</p>
    </div>
    <h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
    <div class="traceback">
      
      <ul><li><div class="frame" id="frame-139756087328976">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">2464</em>,
          in <code class="function">__call__</code></h4>
      <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">    </span>def __call__(self, environ, start_response):</pre>
    <pre class="line before"><span class="ws">        </span>&quot;&quot;&quot;The WSGI server calls the Flask application object as the</pre>
    <pre class="line before"><span class="ws">        </span>WSGI application. This calls :meth:`wsgi_app` which can be</pre>
    <pre class="line before"><span class="ws">        </span>wrapped to applying middleware.&quot;&quot;&quot;</pre>
    <pre class="line current"><span class="ws">        </span>return self.wsgi_app(environ, start_response)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>def __repr__(self):</pre>
    <pre class="line after"><span class="ws">        </span>return &quot;&lt;%s %r&gt;&quot; % (self.__class__.__name__, self.name)</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329552">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">2450</em>,
          in <code class="function">wsgi_app</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">            </span>try:</pre>
    <pre class="line before"><span class="ws">                </span>ctx.push()</pre>
    <pre class="line before"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
    <pre class="line before"><span class="ws">            </span>except Exception as e:</pre>
    <pre class="line before"><span class="ws">                </span>error = e</pre>
    <pre class="line current"><span class="ws">                </span>response = self.handle_exception(e)</pre>
    <pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
    <pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre>
    <pre class="line after"><span class="ws">                </span>raise</pre>
    <pre class="line after"><span class="ws">            </span>return response(environ, start_response)</pre>
    <pre class="line after"><span class="ws">        </span>finally:</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329616">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py"</cite>,
          line <em class="line">272</em>,
          in <code class="function">error_router</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">        </span>if self._has_fr_route():</pre>
    <pre class="line before"><span class="ws">            </span>try:</pre>
    <pre class="line before"><span class="ws">                </span>return self.handle_error(e)</pre>
    <pre class="line before"><span class="ws">            </span>except Exception:</pre>
    <pre class="line before"><span class="ws">                </span>pass  # Fall through to original handler</pre>
    <pre class="line current"><span class="ws">        </span>return original_handler(e)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>def handle_error(self, e):</pre>
    <pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Error handler for the API transforms a raised exception into a Flask</pre>
    <pre class="line after"><span class="ws">        </span>response, with the appropriate HTTP status code and body.</pre>
    <pre class="line after"><span class="ws"></span> </pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329680">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">1867</em>,
          in <code class="function">handle_exception</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">            </span># if we want to repropagate the exception, we can attempt to</pre>
    <pre class="line before"><span class="ws">            </span># raise it with the whole traceback in case we can do that</pre>
    <pre class="line before"><span class="ws">            </span># (the function was actually called from the except part)</pre>
    <pre class="line before"><span class="ws">            </span># otherwise, we just raise the error again</pre>
    <pre class="line before"><span class="ws">            </span>if exc_value is e:</pre>
    <pre class="line current"><span class="ws">                </span>reraise(exc_type, exc_value, tb)</pre>
    <pre class="line after"><span class="ws">            </span>else:</pre>
    <pre class="line after"><span class="ws">                </span>raise e</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">        </span>self.log_exception((exc_type, exc_value, tb))</pre>
    <pre class="line after"><span class="ws">        </span>server_error = InternalServerError()</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329744">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/_compat.py"</cite>,
          line <em class="line">38</em>,
          in <code class="function">reraise</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">    </span>from io import StringIO</pre>
    <pre class="line before"><span class="ws">    </span>import collections.abc as collections_abc</pre>
    <pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">    </span>def reraise(tp, value, tb=None):</pre>
    <pre class="line before"><span class="ws">        </span>if value.__traceback__ is not tb:</pre>
    <pre class="line current"><span class="ws">            </span>raise value.with_traceback(tb)</pre>
    <pre class="line after"><span class="ws">        </span>raise value</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>implements_to_string = _identity</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws"></span>else:</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329296">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">2447</em>,
          in <code class="function">wsgi_app</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">        </span>ctx = self.request_context(environ)</pre>
    <pre class="line before"><span class="ws">        </span>error = None</pre>
    <pre class="line before"><span class="ws">        </span>try:</pre>
    <pre class="line before"><span class="ws">            </span>try:</pre>
    <pre class="line before"><span class="ws">                </span>ctx.push()</pre>
    <pre class="line current"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
    <pre class="line after"><span class="ws">            </span>except Exception as e:</pre>
    <pre class="line after"><span class="ws">                </span>error = e</pre>
    <pre class="line after"><span class="ws">                </span>response = self.handle_exception(e)</pre>
    <pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
    <pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329936">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">1952</em>,
          in <code class="function">full_dispatch_request</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">            </span>request_started.send(self)</pre>
    <pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
    <pre class="line before"><span class="ws">            </span>if rv is None:</pre>
    <pre class="line before"><span class="ws">                </span>rv = self.dispatch_request()</pre>
    <pre class="line before"><span class="ws">        </span>except Exception as e:</pre>
    <pre class="line current"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
    <pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>def finalize_request(self, rv, from_error_handler=False):</pre>
    <pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Given the return value from a view function this finalizes</pre>
    <pre class="line after"><span class="ws">        </span>the request by converting it into a response and invoking the</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330000">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py"</cite>,
          line <em class="line">272</em>,
          in <code class="function">error_router</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">        </span>if self._has_fr_route():</pre>
    <pre class="line before"><span class="ws">            </span>try:</pre>
    <pre class="line before"><span class="ws">                </span>return self.handle_error(e)</pre>
    <pre class="line before"><span class="ws">            </span>except Exception:</pre>
    <pre class="line before"><span class="ws">                </span>pass  # Fall through to original handler</pre>
    <pre class="line current"><span class="ws">        </span>return original_handler(e)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>def handle_error(self, e):</pre>
    <pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Error handler for the API transforms a raised exception into a Flask</pre>
    <pre class="line after"><span class="ws">        </span>response, with the appropriate HTTP status code and body.</pre>
    <pre class="line after"><span class="ws"></span> </pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330064">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">1821</em>,
          in <code class="function">handle_user_exception</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">            </span>return self.handle_http_exception(e)</pre>
    <pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">        </span>handler = self._find_error_handler(e)</pre>
    <pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">        </span>if handler is None:</pre>
    <pre class="line current"><span class="ws">            </span>reraise(exc_type, exc_value, tb)</pre>
    <pre class="line after"><span class="ws">        </span>return handler(e)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>def handle_exception(self, e):</pre>
    <pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Handle an exception that did not have an error handler</pre>
    <pre class="line after"><span class="ws">        </span>associated with it, or that was raised from an error handler.</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329808">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/_compat.py"</cite>,
          line <em class="line">38</em>,
          in <code class="function">reraise</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">    </span>from io import StringIO</pre>
    <pre class="line before"><span class="ws">    </span>import collections.abc as collections_abc</pre>
    <pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">    </span>def reraise(tp, value, tb=None):</pre>
    <pre class="line before"><span class="ws">        </span>if value.__traceback__ is not tb:</pre>
    <pre class="line current"><span class="ws">            </span>raise value.with_traceback(tb)</pre>
    <pre class="line after"><span class="ws">        </span>raise value</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>implements_to_string = _identity</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws"></span>else:</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087329872">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">1950</em>,
          in <code class="function">full_dispatch_request</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">        </span>self.try_trigger_before_first_request_functions()</pre>
    <pre class="line before"><span class="ws">        </span>try:</pre>
    <pre class="line before"><span class="ws">            </span>request_started.send(self)</pre>
    <pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
    <pre class="line before"><span class="ws">            </span>if rv is None:</pre>
    <pre class="line current"><span class="ws">                </span>rv = self.dispatch_request()</pre>
    <pre class="line after"><span class="ws">        </span>except Exception as e:</pre>
    <pre class="line after"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
    <pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>def finalize_request(self, rv, from_error_handler=False):</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330192">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py"</cite>,
          line <em class="line">1936</em>,
          in <code class="function">dispatch_request</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">            </span>getattr(rule, &quot;provide_automatic_options&quot;, False)</pre>
    <pre class="line before"><span class="ws">            </span>and req.method == &quot;OPTIONS&quot;</pre>
    <pre class="line before"><span class="ws">        </span>):</pre>
    <pre class="line before"><span class="ws">            </span>return self.make_default_options_response()</pre>
    <pre class="line before"><span class="ws">        </span># otherwise dispatch to the handler for that endpoint</pre>
    <pre class="line current"><span class="ws">        </span>return self.view_functions[rule.endpoint](**req.view_args)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>def full_dispatch_request(self):</pre>
    <pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Dispatches the request and on top of that performs request</pre>
    <pre class="line after"><span class="ws">        </span>pre and postprocessing as well as HTTP exception catching and</pre>
    <pre class="line after"><span class="ws">        </span>error handling.</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330256">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py"</cite>,
          line <em class="line">468</em>,
          in <code class="function">wrapper</code></h4>
      <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">        </span>:param resource: The resource as a flask view function</pre>
    <pre class="line before"><span class="ws">        </span>&quot;&quot;&quot;</pre>
    <pre class="line before"><span class="ws">        </span>@wraps(resource)</pre>
    <pre class="line before"><span class="ws">        </span>def wrapper(*args, **kwargs):</pre>
    <pre class="line current"><span class="ws">            </span>resp = resource(*args, **kwargs)</pre>
    <pre class="line after"><span class="ws">            </span>if isinstance(resp, ResponseBase):  # There may be a better way to test</pre>
    <pre class="line after"><span class="ws">                </span>return resp</pre>
    <pre class="line after"><span class="ws">            </span>data, code, headers = unpack(resp)</pre>
    <pre class="line after"><span class="ws">            </span>return self.make_response(data, code, headers=headers)</pre>
    <pre class="line after"><span class="ws">        </span>return wrapper</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330320">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/views.py"</cite>,
          line <em class="line">89</em>,
          in <code class="function">view</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">        </span>constructor of the class.</pre>
    <pre class="line before"><span class="ws">        </span>&quot;&quot;&quot;</pre>
    <pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">        </span>def view(*args, **kwargs):</pre>
    <pre class="line before"><span class="ws">            </span>self = view.view_class(*class_args, **class_kwargs)</pre>
    <pre class="line current"><span class="ws">            </span>return self.dispatch_request(*args, **kwargs)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">        </span>if cls.decorators:</pre>
    <pre class="line after"><span class="ws">            </span>view.__name__ = name</pre>
    <pre class="line after"><span class="ws">            </span>view.__module__ = cls.__module__</pre>
    <pre class="line after"><span class="ws">            </span>for decorator in cls.decorators:</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330384">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py"</cite>,
          line <em class="line">583</em>,
          in <code class="function">dispatch_request</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">            </span>decorators = self.method_decorators</pre>
    <pre class="line before"><span class="ws"></span> </pre>
    <pre class="line before"><span class="ws">        </span>for decorator in decorators:</pre>
    <pre class="line before"><span class="ws">            </span>meth = decorator(meth)</pre>
    <pre class="line before"><span class="ws"></span> </pre>
    <pre class="line current"><span class="ws">        </span>resp = meth(*args, **kwargs)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">        </span>if isinstance(resp, ResponseBase):  # There may be a better way to test</pre>
    <pre class="line after"><span class="ws">            </span>return resp</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">        </span>representations = self.representations or OrderedDict()</pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330448">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/examples/owner_app_v1.py"</cite>,
          line <em class="line">97</em>,
          in <code class="function">wrapper</code></h4>
      <div class="source "><pre class="line before"><span class="ws">    </span>@wraps(fn)</pre>
    <pre class="line before"><span class="ws">    </span>def wrapper(*args, **kwargs):</pre>
    <pre class="line before"><span class="ws">        </span>user = request.headers.get(&quot;Authorization&quot;, None)</pre>
    <pre class="line before"><span class="ws">        </span>if user is not None and user.startswith(&quot;User&quot;):</pre>
    <pre class="line before"><span class="ws">            </span># we're completely secure, sir</pre>
    <pre class="line current"><span class="ws">            </span>return fn(*args, **kwargs)</pre>
    <pre class="line after"><span class="ws">        </span>return {&quot;message&quot;: &quot;Unauthorized User&quot;}, 401</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">    </span>return wrapper</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws"></span> </pre></div>
    </div>
    
    <li><div class="frame" id="frame-139756087330128">
      <h4>File <cite class="filename">"/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/Flask_RESTful_DBBase-0.1.6-py3.7.egg/flask_restful_dbbase/resources/collection_model_resource.py"</cite>,
          line <em class="line">45</em>,
          in <code class="function">get</code></h4>
      <div class="source library"><pre class="line before"><span class="ws">        </span>FUNC_NAME = 'get'</pre>
    <pre class="line before"><span class="ws">        </span>name = self.model_class._class()</pre>
    <pre class="line before"><span class="ws">        </span>url = request.path</pre>
    <pre class="line before"><span class="ws">        </span>data = request.args</pre>
    <pre class="line before"><span class="ws">        </span># special - could be a list of fields</pre>
    <pre class="line current"><span class="ws">        </span>order_by = request.args.getlist(&quot;orderBy&quot;, self.order_by)</pre>
    <pre class="line after"><span class="ws"></span> </pre>
    <pre class="line after"><span class="ws">        </span>query = self.model_class.query</pre>
    <pre class="line after"><span class="ws">        </span>if self.process_get_input is not None:</pre>
    <pre class="line after"><span class="ws">            </span>status, result = self.process_get_input(query, data)</pre>
    <pre class="line after"><span class="ws">            </span>if status is False:</pre></div>
    </div>
    </ul>
      <blockquote>AttributeError: 'OrderCollection' object has no attribute 'order_by'</blockquote>
    </div>
    
    <div class="plain">
      <form action="/?__debugger__=yes&amp;cmd=paste" method="post">
        <p>
          <input type="hidden" name="language" value="pytb">
          This is the Copy/Paste friendly version of the traceback.  <span
          class="pastemessage">You can also paste this traceback into
          a <a href="https://gist.github.com/">gist</a>:
          <input type="submit" value="create paste"></span>
        </p>
        <textarea cols="50" rows="10" name="code" readonly>Traceback (most recent call last):
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 2464, in __call__
        return self.wsgi_app(environ, start_response)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 2450, in wsgi_app
        response = self.handle_exception(e)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py&quot;, line 272, in error_router
        return original_handler(e)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 1867, in handle_exception
        reraise(exc_type, exc_value, tb)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/_compat.py&quot;, line 38, in reraise
        raise value.with_traceback(tb)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 2447, in wsgi_app
        response = self.full_dispatch_request()
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 1952, in full_dispatch_request
        rv = self.handle_user_exception(e)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py&quot;, line 272, in error_router
        return original_handler(e)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 1821, in handle_user_exception
        reraise(exc_type, exc_value, tb)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/_compat.py&quot;, line 38, in reraise
        raise value.with_traceback(tb)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 1950, in full_dispatch_request
        rv = self.dispatch_request()
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py&quot;, line 1936, in dispatch_request
        return self.view_functions[rule.endpoint](**req.view_args)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py&quot;, line 468, in wrapper
        resp = resource(*args, **kwargs)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/views.py&quot;, line 89, in view
        return self.dispatch_request(*args, **kwargs)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py&quot;, line 583, in dispatch_request
        resp = meth(*args, **kwargs)
      File &quot;/home/don/proj/web/flask-restful-dbbase/examples/owner_app_v1.py&quot;, line 97, in wrapper
        return fn(*args, **kwargs)
      File &quot;/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/Flask_RESTful_DBBase-0.1.6-py3.7.egg/flask_restful_dbbase/resources/collection_model_resource.py&quot;, line 45, in get
        order_by = request.args.getlist(&quot;orderBy&quot;, self.order_by)
    AttributeError: 'OrderCollection' object has no attribute 'order_by'</textarea>
      </form>
    </div>
    <div class="explanation">
      The debugger caught an exception in your WSGI application.  You can now
      look at the traceback which led to the error.  <span class="nojavascript">
      If you enable JavaScript you can also use additional features such as code
      execution (if the evalex feature is enabled), automatic pasting of the
      exceptions and much more.</span>
    </div>
          <div class="footer">
            Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
            friendly Werkzeug powered traceback interpreter.
          </div>
        </div>
    
        <div class="pin-prompt">
          <div class="inner">
            <h3>Console Locked</h3>
            <p>
              The console is locked and needs to be unlocked by entering the PIN.
              You can find the PIN printed out on the standard output of your
              shell that runs the server.
            <form>
              <p>PIN:
                <input type=text name=pin size=14>
                <input type=submit name=btn value="Confirm Pin">
            </form>
          </div>
        </div>
      </body>
    </html>
    
    <!--
    
    Traceback (most recent call last):
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 2464, in __call__
        return self.wsgi_app(environ, start_response)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 2450, in wsgi_app
        response = self.handle_exception(e)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py", line 272, in error_router
        return original_handler(e)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 1867, in handle_exception
        reraise(exc_type, exc_value, tb)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/_compat.py", line 38, in reraise
        raise value.with_traceback(tb)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 2447, in wsgi_app
        response = self.full_dispatch_request()
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 1952, in full_dispatch_request
        rv = self.handle_user_exception(e)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py", line 272, in error_router
        return original_handler(e)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 1821, in handle_user_exception
        reraise(exc_type, exc_value, tb)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/_compat.py", line 38, in reraise
        raise value.with_traceback(tb)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 1950, in full_dispatch_request
        rv = self.dispatch_request()
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/app.py", line 1936, in dispatch_request
        return self.view_functions[rule.endpoint](**req.view_args)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py", line 468, in wrapper
        resp = resource(*args, **kwargs)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask/views.py", line 89, in view
        return self.dispatch_request(*args, **kwargs)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/flask_restful/__init__.py", line 583, in dispatch_request
        resp = meth(*args, **kwargs)
      File "/home/don/proj/web/flask-restful-dbbase/examples/owner_app_v1.py", line 97, in wrapper
        return fn(*args, **kwargs)
      File "/home/don/proj/web/flask-restful-dbbase/venv/lib/python3.7/site-packages/Flask_RESTful_DBBase-0.1.6-py3.7.egg/flask_restful_dbbase/resources/collection_model_resource.py", line 45, in get
        order_by = request.args.getlist("orderBy", self.order_by)
    AttributeError: 'OrderCollection' object has no attribute 'order_by'
    
    -->

..
