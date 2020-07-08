csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value

getHeaders = function() {
    return {
        headers: {
            "X-CSRFToken": csrf_token
        }
    }
}

var table = new Vue({
    el: '#table',
    delimiters: ["${", "}"],
    data: {
        monitors: [],
        filter: "",
        transProps: {
            name: 'flip-list'
        },
        fields: [{
            key: 'name',
            label: 'Название',
            sortable: true
        },
        {
            key: 'values',
            label: 'Значение',
            sortable: true
        },
        {
            key: 'parameters',
            label: 'Дополнительные параметры',
            sortable: true
        }
    ]
    },
    methods: {},
    created: function(){
        axios.post('/get', {}, getHeaders())
        .then(response => {
            console.log(response)
            this.monitors = response.data
        })
        .catch(error => {
            console.log(error)
        });
    }
})