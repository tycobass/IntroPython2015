(function() {
	window.athst = window.athst || {};
	window.athat = window.athat || (function() {
		var _s = this;
		var _inited = false;
		var _w = window;
		var _d = _w.document;
		var _b = _d.body;
		var _top = _w.top;

		var _init = function() {
			if (_inited) {
				return;
			}
			_inited = true;

			try {
				_top = _w.top.document.location.toString() ? _w.top : _w.self;
			} catch (err) {
				_top = _w.self;
			}

			if (_w.athst.url) {
				_s.url(_w.athst.url);
			}
			if (_w.athst.ifb) {
				_s.ifb(_w.athst.ifb);
			}
			if (_w.athst.tl) {
				_s.tl(_w.athst.tl);
			}
			if (_w.athst.rel) {
				_s.rel(_w.athst.rel);
			}
			if (_w.athst.pop) {
				_s.pop(_w.athst.pop);
			}
			if (_w.athst.layer) {
				_s.layer(_s.athst.layer);
			}
			if (_w.athst.inad) {
				_s.inad(_w.athst.inad);
			}
		};

		var _Curl = function(ad_divid, format_w, format_h, url) {
			var asc = _d.getElementById(ad_divid);
			var asrf = _d.createElement('iframe');
			asrf.id = ad_divid + '_urlif';
			asrf.className = 'al_reset as_frame';
			asrf.width = format_w + 'px';
			asrf.height = format_h + 'px';
			asrf.style.width = format_w + 'px';
			asrf.style.height = format_h + 'px';
			asrf.style.top = '0px';
			asrf.style.left = '0px';
			asrf.src = decodeURIComponent(url);
			asrf.scrolling = 'no';
			asrf.frameBorder = '0';
			asrf.marginWidth = '0px';
			asrf.marginHeight = '0px';
			asc.appendChild(asrf);
		};

		_s.url = function(u) {
			for (var i = 0; i < u.length; ++i) {
				new _Curl(u[i].ad_divid, u[i].format_w, u[i].format_h, u[i].url);
			}
		};

		var _Cifb = function(ifb_url, ifb_time) {
			var _open = function() {
				_w.top.location.replace(ifb_url);
			};
			(ifb_time > 0 && _w.setTimeout(_open, ifb_time * 1000)) || _open();
		};

		_s.ifb = function(b) {
			for (var i = 0; i < b.length; ++i) {
				new _Cifb(b[i]['url'], b[i]['time']);
			}
		};

		_s.tl = function(tls) {
			for (var i = 0; i < tls.ifr.length; ++i) {
				var tl = _d.createElement('iframe');
				tl.width = 0;
				tl.height = 0;
				tl.style.border = 0;
				tl.style.margin = 0;
				tl.scrolling = 'no';
				tl.frameBorder = 0;
				tl.marginWidth = 0;
				tl.marginHeight = 0;
				tl.src = tls.ifr[i];
				_b.appendChild(tl);
			}
			for (var i = 0; i < tls.img.length; ++i) {
				var tl = _d.createElement('img');
				tl.width = 0;
				tl.height = 0;
				tl.border = 0;
				tl.style.border = 0;
				tl.style.margin = 0;
				tl.alt = '';
				tl.src = tls.ifr[i];
				_b.appendChild(tl);
			}
		};

		var _Crel = function(ad_divid, format_w, format_h, http_host, request_id, request_type, clklnk, rel_n, rel_time) {
			var _n = rel_n;
			if (_w.location.hash) {
				var _rel_n = _w.location.hash;
				if (isNaN(_rel_n)) {
					var r = /#(\d*)/.exec(_rel_n);
					_rel_n = r[1];
				}
				if (_rel_n > rel_n) {
					return;
				}
				rel_n = _rel_n;
			}

			var _rel = function() {
				_w.location.hash = rel_n - 1;
				_w.location.replace(_w.location);
				_w.location.reload();
			};

			var _jrel = function() {
				if (_w.athst.url && --_n > 0) {
					var urlif = _d.getElementById(ad_divid + '_urlif');
					if (urlif) {
						urlif.src = http_host + '/s' + request_id + clklnk + '#0';
						_w.setTimeout(_jrel, rel_time * 1000);
					}
					return;
				}
				var asc = _d.getElementById(ad_divid);
				asc.innerHTML = '';
				var asrf = _d.createElement('iframe');
				asrf.className = 'al_reset as_frame';
				asrf.width = format_w + 'px';
				asrf.height = format_h + 'px';
				asrf.style.width = format_w + 'px';
				asrf.style.height = format_h + 'px';
				asrf.style.top = '0px';
				asrf.style.left = '0px';
				asrf.src = http_host + '/s' + request_id + clklnk + '#' + (rel_n - 1);
				asrf.scrolling = 'no';
				asrf.frameBorder = '0';
				asrf.marginWidth = '0px';
				asrf.marginHeight = '0px';
				asc.appendChild(asrf);
			};

			if (rel_n > 0) {
				_w.setTimeout(request_type === 'j' ? _jrel : _rel, rel_time * 1000);
			}
		};

		_s.rel = function(rels) {
			for (var i = 0; i < rels.length; ++i) {
				if (rels[i].rel_n <= 0) {
					continue;
				}
				new _Crel(rels[i].ad_divid, rels[i].format_w, rels[i].format_h, rels[i].http_host, rels[i].request_id, rels[i].request_type, rels[i].clklnk, rels[i].rel_n, rels[i].rel_time);
			}
		};

		var _Cpop = function(pop_url, pop_time, pop_type, pop_width, pop_height) {
			var _shown = false;

			var _pop = function() {
				if (_shown) {
					return;
				}
				var b = _s.gb();

				if (_w.athst.mobile) {
					_fakeA(pop_url, b);
				}
				else {
					_winOpen(pop_url, pop_type === 'under', pop_width, pop_height);
				}
			};

			var _fakeA = function(url, b) {
				_shown = true;
				var _a = _d.createElement('a');
				_a.href = url;
				_a.target = '_blank';
				var _e = _d.createEvent('MouseEvents');
				_e.initMouseEvent('click', true, true, _w, 0, 0, 0, 0, 0, pop_type === 'under' && b !== 'firefox', false, false, false, 0, null);
				_a.dispatchEvent(_e);
			};

			var _winOpen = function(url, focus, width, height) {
				var _win = _top.window.open('about:blank', 'as_' + Math.round(Math.random() * 99999), 'toolbar=1,scrollbars=1,location=1,status=1,statusbar=1,menubar=1,resizable=1,top=0,left=0' + (width && height) ? (',width=' + width + ',height=' + height) : '');
				if (_win) {
					try {
						if (focus) {
							_win.blur();
							_w.blur();
							_w.focus();
						}
					} catch (err) {
					}
					_win.location = url;
					_shown = true;
				}
			};

			if (pop_time < 0) {
				_pop();
				return;
			}

			_w.setTimeout(function() {
				if (_d.addEventListener) {
					_d.addEventListener('click', _pop, false);
					_d.addEventListener('dblclick', _pop, false);
					_d.addEventListener('focus', _pop, false);
					_d.addEventListener('blur', _pop, false);
					_d.addEventListener('resize', _pop, false);
					_d.addEventListener('unload', _pop, false);
					_d.addEventListener('beforeunload', _pop, false);
					_d.addEventListener('orientationchange', _pop, false);
					_d.addEventListener('touchmove', _pop, false);
					_d.addEventListener('touchend', _pop, false);
				}
				else if (_w.attachEvent) {
					_w.attachEvent('onclick', _pop);
					_w.attachEvent('ondblclick', _pop);
					_w.attachEvent('onresize', _pop);
					_w.attachEvent('onunload', _pop);
					_w.attachEvent('onbeforeunload', _pop);
					_w.attachEvent('orientationchange', _pop);
					_w.attachEvent('touchmove', _pop);
					_w.attachEvent('touchend', _pop);
				}
			}, pop_time * 1000);
		};

		_s.pop = function(pops) {
			for (var i = 0; i < pops.length; ++i) {
				new _Cpop(pops[i].pop_url, pops[i].pop_time, pops[i].pop_type, pops[i].pop_width, pops[i].pop_height);
			}
		};

		var _Clayer = function(layer_content, layer_time, layer_type, layer_width, layer_height, layer_close_type, layer_close_url, layer_close_width, layer_close_height) {
			var _moveTimeout = 40;

			var _dHeight = 0;
			var _dWidth = 0;
			var _offsetTop = 0;
			var _startOffsetLeft = 0;
			var _destOffsetLeft = 0;
			var _dx = 0;

			var _init = function() {
				_dHeight = _w.innerHeight;
				_dWidth = _w.innerWidth;
				_offsetTop = _dHeight > layer_height ? parseInt((_dHeight - layer_height) * 0.5) : 0;
				_startOffsetLeft = 0 - (layer_width + 30);
				_destOffsetLeft = _dWidth > layer_width ? parseInt((_dWidth - layer_width) * 0.5) : 0;
				_dx = _destOffsetLeft > _startOffsetLeft ? 20 : -20;
			};

			_init();

			var _reInit = function() {
				_init();
				_adjustAllTops();
			};

			if (_w.addEventListener) {
				_w.addEventListener('resize', _reInit, false);
			}
			else if (_w.attachEvent) {
				_w.attachEvent('onresize', _reInit);
			}

			var _overlay = null, _box = null, _frame = null, _mask = null;

			var _init_container = function() {

				_overlay = _d.createElement('div');
				_overlay.className = 'al_overlay al_reset';
				_overlay.onclick = _close;
				_b.appendChild(_overlay);

				_box = _d.createElement('div');
				_box.className = 'al_box al_reset';
				_box.style.width = layer_width + 'px';
				_box.style.height = layer_height + 'px';
				_box.style.top = _offsetTop + 'px';
				_box.style.left = _startOffsetLeft + 'px';
				_b.appendChild(_box);

				var hideB = _d.createElement('span');
				hideB.className = 'al_close al_link al_reset';
				hideB.onclick = _close;
				_box.appendChild(hideB);

				if (layer_type === 'url') {
					var showB = _d.createElement('span');
					showB.className = 'al_max al_link al_reset';
					showB.onclick = _open;
					_box.appendChild(showB);

					_mask = _d.createElement('div');
					_mask.className = 'al_mask al_reset';
					_mask.style.width = (layer_width + 13) + 'px';
					_mask.style.height = (layer_height + 13) + 'px';
					_mask.style.top = _offsetTop + 'px';
					_mask.style.left = _startOffsetLeft + 'px';
					_mask.onclick = _open;
					_b.appendChild(_mask);
				}
				_frame = _d.createElement('iframe');
				_frame.className = 'al_frame al_reset';
				_frame.style.width = layer_width + 'px';
				_frame.style.height = layer_height + 'px';
				_frame.style.top = (_offsetTop + 6) + 'px';
				_frame.style.left = (_startOffsetLeft + 6) + 'px';
				if (layer_type === 'url') {
					_frame.src = layer_content;
				}

				_frame.scrolling = 'no';
				_frame.frameBorder = '0';
				_frame.marginWidth = '0px';
				_frame.marginHeight = '0px';
				_b.appendChild(_frame);

				if (layer_type === 'script') {
					var ifdoc = _frame.document;
					if (_frame.contentDocument) {
						ifdoc = _frame.contentDocument;
					}
					else if (_frame.contentWindow) {
						ifdoc = _frame.contentWindow.document;
					}

					ifdoc.write(unescape(layer_content));
					ifdoc.onclick = _close;
				}
			};

			var _open = function() {
				if (layer_type === 'url') {
					_w.open(layer_content, '_blank');
				}
				_hide();
			};

			var _close = function() {
				if (layer_close_type === 'root') {
					_top.location.replace(layer_close_url);
				}
				else if (layer_close_type === 'up' || layer_close_type === 'under') {
					new _Cpop(layer_close_url, -1, layer_close_type, layer_close_width, layer_close_height);
				}
				_hide();
			};

			var _hide = function() {
				_overlay.style.display = 'none';
				_box.style.display = 'none';
				_frame.style.display = 'none';
				if (layer_type === 'url') {
					_mask.style.display = 'none';
				}
			};

			var _show = function() {
				_adjustAllTops();

				if (_w.addEventListener) {
					_w.addEventListener('scroll', _adjustAllTops, false);
				}
				else if (_w.attachEvent) {
					_w.attachEvent('onscroll', _adjustAllTops);
				}

				_overlay.style.display = 'block';
				_box.style.display = 'block';
				_frame.style.display = 'block';
				if (layer_type === 'url') {
					_mask.style.display = 'block';
				}

				_w.setTimeout(_move, _moveTimeout);
			};

			var _move = function() {
				var moved = _moveElement(_box, _destOffsetLeft);
				if (layer_type === 'url') {
					moved = _moveElement(_mask, _destOffsetLeft) || moved;
				}
				moved = _moveElement(_frame, _destOffsetLeft + 6) || moved;
				if (moved) {
					_w.setTimeout(_move, _moveTimeout);
				}
			};

			var _adjustTop = function(element, dy, c) {
				element.style.top = (_offsetTop + dy + (typeof c === 'undefined' ? 0 : c)) + 'px';
			};

			var _adjustAllTops = function() {
				var scrollTop = Math.max(_b.scrollTop, _d.documentElement.scrollTop);
				_adjustTop(_box, scrollTop);
				if (layer_type === 'url') {
					_adjustTop(_mask, scrollTop);
				}
				_adjustTop(_frame, scrollTop, 6);
			};

			var _moveElement = function(element, destLeft) {
				var left = parseInt(element.style.left.replace(/px/g, ''));

				if (_dx > 0 && left > destLeft) {
					return false;
				}
				else if (_dx < 0 && left < destLeft) {
					return false;
				}

				element.style.left = (left + _dx) + 'px';
				return true;
			};

			_init_container();
			_w.setTimeout(_show, layer_time * 1000);
		};

		_s.layer = function(layers) {
			for (var i = 0; i < layers.length; ++i) {
				new _Clayer(layers[i].layer_content, layers[i].layer_time, layers[i].layer_type, layers[i].layer_width, layers[i].layer_height, layers[i].layer_close_type, layers[i].layer_close_url, layers[i].layer_close_width, layers[i].layer_close_height);
			}
		};

		var _Cinad = function(src_width, src_height, url, frame_width, frame_height, clkurl, target, clickable, showcorner, start_x, start_y, loop, route, ad_divid) {
			var _top_div = _d.getElementById(ad_divid);
			if (!_top_div) {
				return;
			}

			var _mask_div = _d.createElement('div');
			_mask_div.className = 'al_ia_mask';
			_mask_div.style.height = frame_height + 'px';
			_mask_div.style.width = frame_width + 'px';

			_top_div.appendChild(_mask_div);

			if (showcorner) {
				var _corner_a = _d.createElement('a');
				_corner_a.className = 'al_ia_corner';
				_corner_a.target = target;
				_corner_a.href = clkurl;

				_mask_div.appendChild(_corner_a);
			}

			if (clickable) {
				var _layer_a = _d.createElement('a');
				_layer_a.className = 'al_ia_layer';
				_layer_a.target = target;
				_layer_a.href = clkurl;

				_mask_div.appendChild(_layer_a);
			}

			var _moving_div = _d.createElement('div');
			_moving_div.style.position = 'absolute';
			_moving_div.style.left = start_x + 'px';
			_moving_div.style.top = start_y + 'px';
			_moving_div.style.zIndex = 2;

			var _moving_iframe = _d.createElement('iframe');
			_moving_iframe.scrolling = 'no';
			_moving_iframe.frameBorder = '0';
			_moving_iframe.marginWidth = '0px';
			_moving_iframe.marginHeight = '0px';
			_moving_iframe.style.border = 0;
			_moving_iframe.style.margin = 0;
			_moving_iframe.width = src_width;
			_moving_iframe.height = src_height;
			_moving_iframe.src = url;

			_moving_div.appendChild(_moving_iframe);
			_mask_div.appendChild(_moving_div);

			var pos = 0;
			var len = route.length;

			if (len < 1) {
				return;
			}

			var x = start_x;
			var y = start_y;
			var t = route[pos][2];

			var _move = function() {
				if (!_moving_div) {
					return;
				}
				x = x + route[pos][0];
				y = y + route[pos][1];
				t -= 1;
				_moving_div.style.left = parseInt(x) + 'px';
				_moving_div.style.top = parseInt(y) + 'px';
				if (t <= 0) {
					if (++pos >= len) {
						if (loop) {
							pos = 0;
						}
						else {
							return;
						}
					}
					t = route[pos][2];
					_w.setTimeout(_move, route[pos][4]);
				}
				else {
					_w.setTimeout(_move, route[pos][3]);
				}
			};
			_s.setTimeout(_move, route[pos][4]);
		};

		_s.inad = function(inads) {
			for (var i = 0; i < inads.length; ++i) {
				new _Cinad(inads[i].src_width, inads[i].src_height, inads[i].url, inads[i].frame_width, inads[i].frame_height, inads[i].clkurl, inads[i].target, inads[i].clickable, inads[i].showcorner, inads[i].start_x, inads[i].start_y, inads[i].loop, inads[i].route, inads[i].ad_divid);
			}
		};

		_s.gb = function() {
			var an = _w.navigator['appName'];
			var ua = _w.navigator['userAgent'];
			var mua = ua.match(/(opera|chrome|safari|firefox|msie)/i);
			return (mua ? mua[0] : an).toLowerCase();
		};

		if (!_inited) {
			if (_w.addEventListener) {
				_d.addEventListener('DOMContentLoaded', _init, false);
				_w.addEventListener('load', _init, false);
			}
			else {
				_d.attachEvent('onreadystatechange', _init);
				_w.attachEvent('onload', _init);
			}
		}

		return _s;
	})();
})();
