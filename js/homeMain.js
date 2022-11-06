import fileinfo from "./fileinfo.js"
import recentitem from "./recentitem.js"

Vue.createApp({
    data() {
      return {
        searching:false,
        items:[],
        recentitems:[],
        errMsg:"",
        searchkeyword:""
      }
    }, 
    mounted:function(){
        this.loadRecent();
        var self = this;
        setInterval(function() {
             self.loadRecent();
        }, 5000);
    },
    methods:{
        showAsSearch:function(item){
            this.errMsg = ""
            this.searchkeyword = item.category;
            this.items = [item]
        },
        loadRecent:function(){ 
            var self = this;
            $.ajax({
                method:'GET',
                url:'/api/recent',
                success:function(res){
                    var jres = res ?  res['data'] :[]
                    var result = !jres?[]: Array.isArray(jres) ? jres : [jres];
                    self.recentitems = result
                },
                error:function(ex){
                    //showError("Something went wrong.");
                },
                complete:function(){

                }
            });
        },
        performSearch: function(e) {
            if(e){
                e.preventDefault();
            }
            this.items = []
            var self = this;
            self.errMsg = "";
            var searchword = this.searchkeyword
            if(!searchword){
                self.errMsg = "Provide something to search"; 
                return;
            }  
            this.searching= true
            //showLoading();
            var searchAPI = '/api/search';

            $.ajax({
                method:'POST',
                url:searchAPI,
                contentType:'application/json',
                data:JSON.stringify({
                    searchKeyWord: searchword
                }),
                success:function(res){
                    var jres = res ?  res['data'] :[]
                    var result = !jres?[]: Array.isArray(jres) ? jres : [jres];
                   // renderItems( result)
                   self.items = result
                },
                error:function(ex){
                    showError("Something went wrong.");
                },
                complete:function(){
                    self.searching = false
                }
            });
        }
    },
    components:{fileinfo,recentitem}
  }).mount('#app')