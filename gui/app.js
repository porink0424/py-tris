const app = new Vue({
    el: "#app",
    data: {
        mode: 'inApp',
        multiPlay: false,
        quickSearch: false,
        expression: "利用したいコントローラー（もしくはキーボード）を1Pに設定した上で、「開始」を押す",
        python: null,
    },
    methods: {
        Start() {
            axios.get('http://localhost:3000/api/start', {
                params: {
                    mode: this.mode,
                    multiPlay: this.multiPlay,
                    quickSearch: this.quickSearch,
                }
            })
                .then(response => {
                    console.log(JSON.stringify(response.data));
                });
        },
        Stop() {
            axios.get('http://localhost:3000/api/stop')
                .then(response => {
                    console.log(JSON.stringify(response.data));
                });
        }
    },
});
