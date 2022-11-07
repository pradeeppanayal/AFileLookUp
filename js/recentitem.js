const template = `<div class="card mb-3" @click="emitSelection" style="cursor:pointer;">
                    <div class="row no-gutters"> 
                            <div class="col-md-4">   
                                   <img style="width:100%; height:100%" :src="'/api/'+item.category+'/'+item.imageFile" class="card-img" alt="..."> 
                            </div>              
                            <div class="col-md-8">                  
                                <div class="card-body">                      
                                    <h6 class="card-title">{{item.category}}</h6>
                                </div>
                            </div>
                    </div>
                </div>`

export default {
    props:["item"],
    template,
    methods:{
        emitSelection:function(){
            this.$emit('selection',this.item);
        }
    }
}