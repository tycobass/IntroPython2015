(function () {
    _(
        {"status":{"code":"OK"},"jsVersion":"15.47.147","id":"564b4494e4b0e3797a7bf581","wlcid":"5511b338e4b0856472fb903b","bid":{"id":"5512829de4b006f4584d22eb","videos":[{"videoId":"5580078ce4b026306dd518e0","name":"Explore- V2","videoUrls":["http://cdn.vidible.tv/prod/2015-06/16/5580078ce4b026306dd518e0_480x270_v1.mp4","http://cdn.vidible.tv/prod/2015-06/16/5580078ce4b026306dd518e0_480x270_v1.ogg"],"thumbnailId":"56138f42b66dfa93401cf34f","thumbnail":"http://cdn.vidible.tv/prod/2015-06/16/5580078ce4b026306dd518e0_60x60_A_v1.png","fullsizeThumbnail":"http://cdn.vidible.tv/prod/2015-06/16/5580078ce4b026306dd518e0_480x270_A_v1.png","subtitles":[],"captions":{},"metadata":{"duration":48298,"clickurl":"http://www.watch4.com/","clickableTimeInSeconds":0,"commonRating":{"value":"G","descriptors":[],"minAge":0}},"videoSourceType":"FILE","studioName":"Ludius Media","cs":{"p":false}}]},"playerTemplate":{"initialization":"autoplay","sound":"muted","initialVolume":0.01,"videosToPlay":2000,"videosToRequest":1,"shuffleVideos":false,"prerollFrequency":0,"backgroundSkin":"http://cdn.vidible.tv/prod/2015-04/15/552e6344e4b01f589d051ab4_v1.png","backgroundSkinLocation":{"x":0,"y":0,"w":300,"h":250},"controlsSkin":"http://cdn.vidible.tv/prod/player/swf/15.47.142/ControlsNDN 10 without Fullscreen.swf","controlsSkinLocation":{"x":0,"y":265,"w":400,"h":0},"videoLocation":{"x":0,"y":0,"w":400,"h":300},"afterVideosUI":"next","scrubBarSkin":"http://cdn.vidible.tv/prod/2013-03/10/511e8160e4b0bf40bd0340a7_v2.swf","coveringsSkin":"http://cdn.vidible.tv/prod/player/swf/15.47.142/Coverings.swf","coveringsSkinLocation":{"x":0,"y":0,"w":400,"h":300},"surroundSkinLocation":{"x":0,"y":0,"w":0,"h":0},"playerWidth":400,"playerHeight":300,"controlsAutoPosition":true,"controlsChromeless":true,"controlsBackgroundAlpha":"1.0","controlsConfig":{"colorSchema":{"mainColor":{"backgroundAlpha":1.0}}},"nielsenSiteCampaign":"cmp185272","nielsenChannelCampaign":"cmp185273","backgroundFill":false,"backgroundColor":0,"surround3DBevelShadowColor":16777215,"surround3DBevelHighlightColor":16777215,"surroundInnerRadius":0,"surroundCornerRadius":0,"surroundHole":false,"surround3D":false,"surround3DBevelSize":0,"surround3DBevelStrength":0.0,"extras":[{"region":{"x":0,"y":0,"w":0,"h":0},"blocking":true,"urls":{"FLASH":"http://cdn.vidible.tv/prod/player/swf/15.47.142/click-throughs.swf"}}],"publisherPayout":"None","publisherAmount":0.0,"metaData":{},"showLogo":false,"HLSExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/hls-plugin.swf","IMAExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/ima-ad-module.swf","YuMeExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/yume-ad-module.swf","FreeWheelExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/free-wheel-module.swf","VASTExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/vast-ad-engine.swf","PlayerAdSystem":"http://cdn.vidible.tv/prod/player/swf/15.47.142/vidible-ad-server.swf","UIExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/controls-sticky.swf","AgeGateExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/age-gate.swf","SubtitlesExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/subtitles.swf","ClickExtra":"http://cdn.vidible.tv/prod/player/swf/15.47.142/click-throughs.swf"},"adSettings":{"podSize":1,"prerollInterleave":2,"midrollTiming":"5%;10%;15%;20%;25%;30%;35%;40%;45%;50%;55%;60%;65%;70%;75%;80%;85%;90%;95%","softTimeout":0.4,"hardTimeout":3.2,"startTimeout":19.200000000000003,"domainOptimisation":true,"adStrategy":"ADSET_BASED","companions":[],"aeg":[],"asids":["564c6973e4b022fdd6ccfc57"]},"playerWidget":{"playerType":"SMART","url":"http://cdn.vidible.tv/prod/player/swf/15.47.142/player-vast.swf","adOnly":false,"isAol":false},"geo":{"country":"usa","region":"wa","zipCode":"98115","areaCode":"206","connSpeed":"cable"},"brandedContent":false}
    );
    function _(json) {
                    /*
     Developed by Robert Nyman, http://www.robertnyman.com
     Code/licensing: http://code.google.com/p/getelementsbyclassname/
     */
            var getElementsByClassName = function (className, tag, elm) {
                if (document.getElementsByClassName) {
                    getElementsByClassName = function (className, tag, elm) {
                        elm = elm || document;
                        var elements = elm.getElementsByClassName(className),
                            nodeName = (tag) ? new RegExp("\\b" + tag + "\\b", "i") : null,
                            returnElements = [],
                            current;
                        for (var i = 0, il = elements.length; i < il; i += 1) {
                            current = elements[i];
                            if (!nodeName || nodeName.test(current.nodeName)) {
                                returnElements.push(current);
                            }
                        }
                        return returnElements;
                    };
                }
                else if (document.evaluate) {
                    getElementsByClassName = function (className, tag, elm) {
                        tag = tag || "*";
                        elm = elm || document;
                        var classes = className.split(" "),
                            classesToCheck = "",
                            xhtmlNamespace = "http://www.w3.org/1999/xhtml",
                            namespaceResolver = (document.documentElement.namespaceURI === xhtmlNamespace) ? xhtmlNamespace : null,
                            returnElements = [],
                            elements,
                            node;
                        for (var j = 0, jl = classes.length; j < jl; j += 1) {
                            classesToCheck += "[contains(concat(' ', @class, ' '), ' " + classes[j] + " ')]";
                        }
                        try {
                            elements = document.evaluate(".//" + tag + classesToCheck, elm, namespaceResolver, 0, null);
                        }
                        catch (e) {
                            elements = document.evaluate(".//" + tag + classesToCheck, elm, null, 0, null);
                        }
                        while ((node = elements.iterateNext())) {
                            returnElements.push(node);
                        }
                        return returnElements;
                    };
                }
                else {
                    getElementsByClassName = function (className, tag, elm) {
                        tag = tag || "*";
                        elm = elm || document;
                        var classes = className.split(" "),
                            classesToCheck = [],
                            elements = (tag === "*" && elm.all) ? elm.all : elm.getElementsByTagName(tag),
                            current,
                            returnElements = [],
                            match;
                        for (var k = 0, kl = classes.length; k < kl; k += 1) {
                            classesToCheck.push(new RegExp("(^|\\s)" + classes[k] + "(\\s|$)"));
                        }
                        for (var l = 0, ll = elements.length; l < ll; l += 1) {
                            current = elements[l];
                            match = false;
                            for (var m = 0, ml = classesToCheck.length; m < ml; m += 1) {
                                match = classesToCheck[m].test(current.className);
                                if (!match) {
                                    break;
                                }
                            }
                            if (match) {
                                returnElements.push(current);
                            }
                        }
                        return returnElements;
                    };
                }
                return getElementsByClassName(className, tag, elm);
            };
            var cl = "vdb_564b4494e4b0e3797a7bf5815511b338e4b0856472fb903b";
            var c = getElementsByClassName(cl, null, document.body)[0];
            c.className = c.className.replace(new RegExp("(\\s*)" + cl + "\\s*", "g"), "$1");
                var p = (c.getAttribute("vdb_params") || "") + "";

        var cb = /(?:[\?&]|^)m\.cb=(.*?)(&m\..*?=|$)/g.exec(p);
        cb = cb && cb[1] || Math.random();
        var ur = /(?:[\?&]|^)m\.url=(.*?)(&m\..*?=|$)/g.exec(p);
        ur = ur && ur[1];
        function ee(pn, v, dv) {
            var ve = dv && dv(v) || v;
            if (ve == v) {
                try {
                    ve = decodeURIComponent(v);
                    ve = encodeURIComponent(ve);
                } catch (e) {
                    ve = encodeURIComponent(v);
                }
            }
            p = p.replace("m." + pn + "=" + v, "m." + pn + "=" + ve);
            v = ve;
            return v;
        }

        ee("url", ur);
        p += p && "&";
        var ifr = window != top;
        var r = encodeURIComponent(ifr ? document.referrer : location.href);
        var i = document.createElement("img");
        var it = new Date().getTime();
                                    var si = c.getElementsByTagName('img');
                var srcSubstr = 'http://trk.vidible.tv/trk/impression.gif';
                var isImpressionExist = false;
                for (var ik = 0; ik < si.length; ik++) {
                    if (si[ik].src.indexOf(srcSubstr) !== -1) {
                        isImpressionExist = true;
                        break;
                    }
                }
                if (!isImpressionExist) {
                    i.src = "http://trk.vidible.tv/trk/impression.gif?pid=564b4494e4b0e3797a7bf581&bcid=5511b338e4b0856472fb903b&" + p + "ifr=" + ifr + "&cb=" + cb + "&r=" + r + "&recover=true";
                    i = document.createElement("img");
                    var et = encodeURIComponent('player error');
                    var st = encodeURIComponent('workflow error');
                    var dt = encodeURIComponent('Static impression was removed');
                    i.src = "http://trk.vidible.tv/trk/error.gif?pid=564b4494e4b0e3797a7bf581&bcid=5511b338e4b0856472fb903b&" + p + "ifr=" + ifr + "&cb=" + cb + "&r=" + r + "&et=" + et + "&st=" + st + "&dt=" + dt;
                    i = document.createElement("img");
                }
                            i.src = "http://trk.vidible.tv/trk/js-loaded.gif?pid=564b4494e4b0e3797a7bf581&bcid=5511b338e4b0856472fb903b&" + p + "ifr=" + ifr + "&cb=" + cb + "&r=" + r;
                var s = document.createElement("script");
        s.type = "text/javascript";
                    s.src = "http://cdn.vidible.tv/prod/player/js/15.47.147/vidible-min.js?pid=564b4494e4b0e3797a7bf581&bcid=5511b338e4b0856472fb903b&" + p + "ifr=" + ifr + "&cb=" + cb + "&r=" + r;
                s.onload = function () {
                            var pl = vidible.createPlayer({apid: "", pid: "564b4494e4b0e3797a7bf581", bcid: "5511b338e4b0856472fb903b",  params: p, content: c, it: it, site: r}, json, {"cdn":"http://cdn.vidible.tv/prod/","trk":"http://trk.vidible.tv/trk/","ds":"http://delivery.vidible.tv/","ads":"http://ads.vidible.tv/","adt":"http://ads.vidible.tv/","ptv":"http://portal.vidible.tv/"});
                                        var i = document.createElement("img");
                i.src = "http://trk.vidible.tv/trk/js-started.gif?pid=564b4494e4b0e3797a7bf581&bcid=5511b338e4b0856472fb903b&" + p + "ifr=" + ifr + "&cb=" + cb + "&r=" + r;
                        var clb =  window['vidibleInitialize'];
            if (clb) {
                clb(pl);
            }
            s.onload = s.onreadystatechanged = function () {
            };
        };
        s.onreadystatechange = function () {
            if (s.readyState == 'complete' || s.readyState == 'loaded') {
                s.onload();
            }
        };
        c.appendChild(s);
    }
})();
