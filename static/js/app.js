
(function () {
    var WikiSearch = {};
    WikiSearch.queryParams = {};
    WikiSearch.setupWikiSearch = function () {
        var searchElement = document.getElementById('q');
        searchElement.addEventListener('keyup', this.keyUpCallBack.bind(this));
        WikiSearch.queryParams = fetchQueryParams();
        searchElement.value = this.queryParams['q'] || '';
//        if(searchElement.value){
//            this.fetchWikis(searchElement.value,this.queryParams['offset']||0,this.queryParams['limit']||10);
//        }
    }

    WikiSearch.autoSearchWiki = function (responseText) {
        var responseJson = responseText ? JSON.parse(responseText) : {};
        console.log('responseJson ==>> ', responseJson);
        if (responseJson && responseJson['query'] && responseJson['query'].search &&
            responseJson['query'].search.length > 0) {
            var typeAheadResults = responseJson['query'].search;
            var autoComplete = document.getElementById('wiki-search-data');
            autoComplete.innerHTML = '';
            typeAheadResults = Object.values(typeAheadResults);
            typeAheadResults.forEach((eachObject) => {
                var divTag = document.createElement('div');
                divTag.classList.add('row');
                var aTag = document.createElement('a');
                aTag.setAttribute('href', '/article?pageid=' + eachObject['pageid']);
                aTag.innerHTML = eachObject['title'];
                divTag.appendChild(aTag);
                autoComplete.appendChild(divTag);
            });
        }
    }

    WikiSearch.keyUpCallBack = function (event) {
        console.log('event', event.target.value, 'event name', event.type);
        if (event.target.value && event.target.value.length >= 3) {
            this.fetchWikis(event.target.value,0,5);
        }
    }

    WikiSearch.fetchWikis = function(value,offset,limit){
        var url = "http://localhost:8000/type_ahead_wikis/";
        var params = {
            'action': 'query',
            'q': value,
            'offset':offset,
            'format': 'json',
            'list': 'search',
            'limit': limit
        }

        this.processAjaxCall.call(this, url, params, 'GET', this.autoSearchWiki.bind(this));
    }

    WikiSearch.processAjaxCall = function (url, params, method, callback) {

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                callback(this.responseText);
            }
        };

        if (method === 'GET') {
            url = url + '?' + paramsToQueryString(params);
            xhttp.open(method, url);
            xhttp.setRequestHeader('Access-Control-Allow-Origin', '*');
            xhttp.send();
        } else if (method === 'POST') {
            xhttp.open(method, url);
            xhttp.setRequestHeader('Access-Control-Allow-Origin', '*');
            xhttp.send(params);
        }

    }

    function paramsToQueryString(params) {
        var queries = [];
        for (eachParam in params) {
            queries.push(encodeURIComponent(eachParam) + "=" + encodeURIComponent(params[eachParam]));
        }
        return queries.join('&');
    }

    function fetchQueryParams(){
        var currentUrl = window.location.href;
        currentUrl = currentUrl.replace(new RegExp("\\+","g"),'%20');
        var querySplitter = currentUrl.split('?');
        var queryString = querySplitter && querySplitter.length ? querySplitter[1]:''
        queryString = decodeURIComponent(queryString);
        var queryParamsValues = queryString.split('&');
        var queryParams = {};
        queryParamsValues.forEach(eachQueryValue => {
            var querySplit = eachQueryValue.split('=');
            queryParams[querySplit[0]] = querySplit[1];
        });
        return queryParams;
    }

    function constructPaginationLinks(totalHits){
        var pagination = document.getElementById('pagination');
        var displayableLinks = 20;

        for(var i = 0;i<displayableLinks;i++){
            var eachPaginatedLink = document.createElement('a');
            eachPaginatedLink.classList.add('.button');
            eachPaginatedLink.innerHTML = (i+1);
            var params ={
                'action': 'query',
                'srsearch': value,
                'sroffset':offset,
                'format': 'json',
                'list': 'search',
                'srlimit': limit,
            }
            var queryString = paramsToQueryString(params);
            eachPaginatedLink.setAttribute('href','/article.html?'+queryString);
            pagination.appendChild(eachPaginatedLink);
        }

    }

    WikiSearch.setupWikiSearch();

})();