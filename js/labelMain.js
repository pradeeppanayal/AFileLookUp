import filelabel from './label.js'

Vue.createApp({
    data() {
      return { 
        fileinfo:undefined,
        passedFileId:"",
        nlabelname:"",
        loading:false
      }
    }, 
    mounted:function(){ 
        this. passedFileId = this.getSearchParams('fileid');
        this.loadLabels();
    },
    methods:{
        addlabel:function(e){
            if(e) e.preventDefault();
            var label = this.nlabelname;
            if(!label){
                return;
            }
            var self = this;
            self.nlabelname = "";
            $.ajax({
                url:"/api/fileinfo/"+self.passedFileId+"/labels",
                method:'POST',
                data:JSON.stringify({'label':label}),
                contentType:'application/json',
                success:function(e){
                    self.loadLabels();
                },
                error:function(){
                    //$('#loading').css('display','none');
                },
            })
        },
        getSearchParams:function(k){
            var p={};
            location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi,function(s,k,v){p[k]=v})
            return k?p[k]:p;
        },
        loadLabels : function(){
            var self = this;
            self.loading = true;
            self.fileinfo= undefined;
            $.ajax({
                url:"/api/fileinfo/"+self.passedFileId,
                success:function(e){
                    var item = e.data
                    if(!item){ 
                        return;
                    }
                    self.fileinfo = item
                    $('body').css('background-image','url(/api/'+self.fileinfo.category+'/'+self.fileinfo.imageFile+')');
                    
                },
                complete:function(){
                    self.loading =false;
                }
            });
        },
        deleteLabel : function(item){
            if(!item) return;
            var self = this; 
    
            $.ajax({
                url:'/api/fileinfo/'+self.passedFileId+'/labels/'+item.id,
                contentType:'application/json',
                method:'DELETE',
                data:JSON.stringify({}),
                complete:function(){
    
                },
                success:function(){
                    self.loadLabels();
                }
            });
        }
    },
    components:{filelabel}
  }).mount('#app')