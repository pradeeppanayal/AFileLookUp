  export default {
    props:["item"],
    data() {
      return {
        count: 0
      }
    },
    template:`<div class="card" style="width: 18rem;" v-if="item">
    <img title="View the full size image" :src="'/api/'+item.category+'/'+item.imageFile" class="card-img-top" style="cursor:pointer;" @click="openImage" alt="No photo">
    <div class="card-body">
      <h5 class="card-title">{{item.category}}
        <a :href="'labels?fileid='+item.id">
            <img style="width:25px; float:right; cursor:pointer;" title="Edit labels" src="/web/asset/img/label.png" alt="Manage labels">
        </a>
      </h5>
      <p class="card-text"></p>
      <input title="Click to edit the vector file" @click="openVector" type="button" href="" class="btn btn-primary btn-lg btn-block" value="Edit">
    </div>
  </div>`,
  methods:{
      openVector:function(){
        this.openInAppTrigger(this.item.category, this.item.vectorFile)
      },
      openImage:function(){
        this.openInAppTrigger(this.item.category, this.item.imageFile)
      },
      openInAppTrigger: function(category, filename){
        var api  = '/api/'+category+'/'+ filename+"/openinapp"
        $.ajax({
          url:api,
          method:'GET',
          success:function(e){
            console.log("triggerd file open "+ filename+" of the category "+ category)
          },
          error:function(e){
            showError("Could not triggerd file open "+ filename+" of the category "+ category)
          }
        });
    }
  }
}
 