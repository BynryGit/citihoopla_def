






	/*			 var start1 = $("#start"+i).kendoTimePicker().data("kendoTimePicker");
			    var end1 = $("#end"+i).kendoTimePicker().data("kendoTimePicker");
			    $('.sel2').select2();

			    start1 = $("#start"+i).kendoTimePicker({
                        change: startChange
                    }).data("kendoTimePicker");

			                    //define min/max range
			                    start1.min("8:00 AM");
			                    start1.max("6:00 PM");

			                    //define min/max range
			                    end1.min("8:00 AM");
			                    end1.max("7:30 AM");



				 } */







				var subcat_list = []
	 			// Validations Start-------------------------->
				function check_Subcategory(){
				//alert('hello');
				isValid = false;
					$('.subcat_select').each(function(){
						//alert('SubCat Value: '+$(this).val());
						if($(this).val()=='' && $(this).attr('required')){
						//alert('If: '+$(this).val());
						$(this).parent().children('.error').css("display", "block");
			    			$(this).parent().children('.error').text("Please select Sub Category");
			    			isValid = false;
			    			return false;
						}else{
						//alert('Else: '+$(this).val());
							 $(this).parent().children('.error').css("display", "none");
							 //subcat_list.push($(this).val());
							 //alert('Pushing... '+subcat_list);
							 isValid = true;
							 return true;
						}
					});
					return isValid;
				}


	 			function checkCateg(categ){

			  if($(categ).val()!='' && $(categ).val()!=null)
			   {
			    $(categ).parent().children('.error').css("display", "none");
			   var subcat_result = check_Subcategory();
			    //alert('Result: '+subcat_result);
			    if(check_Subcategory()==true){
			    		//alert('true');
						return true;
			    }
			    else{
			    //alert('false');
			    	return false;
			    }
			   }else{
			    $(categ).parent().children('.error').css("display", "block");
			    $(categ).parent().children('.error').text("Please select Advert Category");
			   return false;
			   }
			    return false;
			}

function checkAdverttitle(advert_title){
    var namePattern = /[A-Za-z]+/;
    var advert_titl = $(advert_title).val() ;
    if(namePattern.test(advert_titl) ){
        $(advert_title).parent().children('.error').css("display", "none");
        return true;
    }else if(advert_titl==''){
        $(advert_title).parent().children('.error').css("display", "block");
        $(advert_title).parent().children('.error').text("Please enter  Advert Title");
        return false;
    }else{
        $(advert_title).parent().children('.error').css("display", "block");
        $(advert_title).parent().children('.error').text("Please enter valid Advert Title");
    }
    return false;
}

		function checkWebsite(website){

			Website = $(website).val()
		   var namePattern = /(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})/;
		 	 if(Website=='')
			{
			return true;
			}
		   else if(namePattern.test(Website)){
		      $(website).parent().children('.error').css("display", "none");
		   return true;
		   }else{
		 	$(website).parent().children('.error').css("display", "block");
		   $(website).parent().children('.error').text("Please enter valid Website");
		   return false;
		   }
		}

		function checkShortDesc(business){
			if($(short_discription).val()!='')
		   {
		    $( short_discription).parent().children('.error').css("display", "none");
		   return true;
		   }else{
		    $( short_discription).parent().children('.error').css("display", "block");
		    $( short_discription).parent().children('.error').text("Please enter Short Description");
		   return false;
		   }
		}

		  function checkProductPrice(product_price_cls){
				var isValid = true;

			   $(product_price_cls).each(function( index ) {


						var product_price_cls = $(this).val();
						var parentvalue = $(this).parent().parent().prev('div').find('.product_name_cls').val() ;
									if( parentvalue != "") {

							 	  		if(product_price_cls ==''){

			 	  						$(this).parent().children('.error').css("display", "block");
		 								$(this).parent().children('.error').text("Please enter Product Price ");
		 								isValid = false;
		 								return false ;

							 	  	}else{
						   				$(this).parent().children('.error').css("display", "none");
						   				isValid = true;
				    						return true ;
							   		}
					   		}


				});
		 return isValid;

			}


  function checkProductName(product_name_cls){
				var isValid = true;

			   $(product_name_cls).each(function( index ) {


						var product_name_cls = $(this).val();
						var parentvalue = $(this).parent().parent().next('div').find('.product_price_cls').val() ;

									if( parentvalue != "") {

							 	  		if(product_name_cls ==''){

			 	  						$(this).parent().children('.error').css("display", "block");
		 								$(this).parent().children('.error').text("Please enter Product Name ");
		 								isValid = false;
		 								return false ;

							 	  	}else{
						   				$(this).parent().children('.error').css("display", "none");
						   				isValid = true;
				    						return true ;
							   		}
					   		}


				});
		 return isValid;

			}


	function checkPhoneCateg(phone_type){

   	var isValid = false;
		 $(phone_type).each(function( index ) {

			if(index==0){
			  if($(this).select2("val")!='0')
			   {
			    $(this).parent().children('.error').css("display", "none");
				 		isValid = true;
			   }else{
			    $(this).parent().children('.error').css("display", "block");
			    $(this).parent().children('.error').text("Please select Phone Category ");
			    isValid = false;
			   return false;
			   }
			 }
			 else{
			  if($(this).select2("val")!='0')
			   {
			    $(this).parent().children('.error').css("display", "none");
				 		isValid = true;
			   }else{

			    isValid = true;
			   return true;
			   }

			 }

			 });

			 return isValid;
			}

function checkPhoneNumber(phone_number){
    var isValid = false;
    $(phone_number).each(function( index ) {
        if(index==0){
            var	phoneno = $(this).val()
                if($(this).parent().parent().prev('div').find('select').val()==3) {
                    var phoneNumberPattern = /^[789]\d{9}$/;

                    if(phoneNumberPattern.test(phoneno)){
                        $(this).parent().children('.error').css("display", "none");
                        isValid = true;
                    }
                    else{
                        $(this).parent().children('.error').css("display", "block");
                        $(this).parent().children('.error').text("Please enter valid Phone Number");
                        isValid = false;
                    }
                }else if($(this).parent().parent().prev('div').find('select').val()==4){
                    var phoneNumberPattern = /^[0123456789]\d{10}$/;
                    if(phoneNumberPattern.test(phoneno)){
                        $(this).parent().children('.error').css("display", "none");
                        isValid = true;
                    }else{
                        $(this).parent().children('.error').css("display", "block");
                        $(this).parent().children('.error').text("Please enter valid Phone Number");
                        isValid = false;
                    }
                }else{

                    $(this).parent().children('.error').css("display", "block");
                    $(this).parent().children('.error').text("Please enter  Phone Number");
                    isValid = false;

                }
        }else{
            var	phoneno = $(this).val()
            if($(this).parent().parent().prev('div').find('select').val()==3) {
                var phoneNumberPattern = /^[789]\d{9}$/;

                if(phoneNumberPattern.test(phoneno)){
                    $(this).parent().children('.error').css("display", "none");
                    isValid = true;
                }
                else{
                //$(this).parent().children('.error').css("display", "block");
                //$(this).parent().children('.error').text("Please enter valid Phone Number");
                    if(phoneno == ""){
                        $(this).parent().children('.error').css("display", "none");
                        isValid = true;
                    }
                    else{
                        $(this).parent().children('.error').css("display", "block");
                        $(this).parent().children('.error').text("Please enter valid Phone Number");
                        isValid = false;
                        return true;
                    }
                }
            }else if($(this).parent().parent().prev('div').find('select').val()==4){
                var phoneNumberPattern = /^[0123456789]\d{10}$/;
                if(phoneNumberPattern.test(phoneno)){
                    $(this).parent().children('.error').css("display", "none");
                    isValid = true;
                }else{

                    if(phoneno == ""){
                        $(this).parent().children('.error').css("display", "none");
                        isValid = true;
                    }
                    else{
                        $(this).parent().children('.error').css("display", "block");
                        $(this).parent().children('.error').text("Please enter valid Phone Number");
                        isValid = false;
                        return true;
                    }
                }
            }else{
                isValid = true;
            }
        }
    });
    return isValid;
}

			function checkEmail(email_primary){
				Email = $(email_primary).val()
			   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;

			   if(namePattern.test(Email)){
			      $(email_primary).parent().children('.error').css("display", "none");
			   return true;
			   }else if(Email==""){
			   	$(email_primary).parent().children('.error').css("display", "block");
			   	$(email_primary).parent().children('.error').text("Please enter  Email");

			   }
			   else {
			 	$(email_primary).parent().children('.error').css("display", "block");
			   $(email_primary).parent().children('.error').text("Please enter valid Email");
			   return false;
			   }
			}

			function checkSecEmail(email_secondary){

			Email = $(email_secondary).val()
		   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;
		 	 if(Email=='')
			{
			return true;
			}
		   else if(namePattern.test(Email)){
		      $(email_secondary).parent().children('.error').css("display", "none");
		   return true;
		   }else{
		 	$(email_secondary).parent().children('.error').css("display", "block");
		   $(email_secondary).parent().children('.error').text("Please enter valid Email");
		   return false;
		   }
		}

		function checkaddress(address_line1){

			if($(address_line1).val()!='')
		   {
		    $(address_line1).parent().children('.error').css("display", "none");
		   return true;
		   }else{
		    $(address_line1).parent().children('.error').css("display", "block");
		    $(address_line1).parent().children('.error').text("Please enter  Address");
		   return false;
		   }
		}


		function checkArea(area){

			Area = $(area).val()
		   var namePattern = /^[0-9]*$/;
		 	 if(Area=='')
			{
			$(area).parent().children('.error').css("display", "block");
		  	 	$(area).parent().children('.error').text("Please enter  Area");
			return false;
			}
		   else if(namePattern.test(Area)){
		   	$(area).parent().children('.error').css("display", "block");
		  	 	$(area).parent().children('.error').text("Please enter valid Area");

		   return false;
		   }else{
		 	$(area).parent().children('.error').css("display", "none");
		   return true;
		   }
		}


			function checkLandmark(landmark){

			Landmark = $(landmark).val()
		   var namePattern = /^[0-9]*$/;
		 	 if(Landmark=='')
			{
			return true;
			}
		   else if(namePattern.test(Landmark)){
		   	$(landmark).parent().children('.error').css("display", "block");
		  	 	$(landmark).parent().children('.error').text("Please enter valid Landmark");

		   return false;
		   }else{
		 	$(landmark).parent().children('.error').css("display", "none");
		   return true;
		   }
		}


		function checkState(statec){

			statec1 = $("#statec").val();


		 	 if(statec1 == '' || statec1 == null)
			{
			$(statec).parent().children('.error').css("display", "block");
		  	 	$(statec).parent().children('.error').text("Please select State");
			return false;
			}
		   else{
		 	$(statec).parent().children('.error').css("display", "none");
		   return true;
		   }
		}


			function checkCity(city){

			city1 = $("#city").val();


		 	 if(city1 == '' || city1 == null)
			{
			$(city).parent().children('.error').css("display", "block");
		  	 	$(city).parent().children('.error').text("Please select City");
			return false;
			}
		   else{
		 	$(city).parent().children('.error').css("display", "none");
		   return true;
		   }
		}

			function checkPincode(statec){

			pincode1 = $("#pincode").val();


		 	 if(pincode1 == '' || pincode1 == null)
			{
			$(pincode).parent().children('.error').css("display", "block");
		  	 	$(pincode).parent().children('.error').text("Please select Pincode");
			return false;
			}
		   else{
		 	$(pincode).parent().children('.error').css("display", "none");
		   return true;
		   }
		}



		//Real Estate Validation

        function check_market_rate(){
         var isValid = false;
                if($("#pro_mark_rate").val() =="")
                {

                    $("#pro_mark_rate").parent().children('.error').css("display", "block");
                    $("#pro_mark_rate").parent().children('.error').text("Please enter Property Market Rate");
                  isValid = false;
               }else{

                    $("#pro_mark_rate").parent().children('.error').css("display", "none");
                isValid =  true;
               }
               return isValid;

        }

            function check_poss_status(){
         var isValid = false;
                if($("#possesion_status").val() ==""  || $("#possesion_status").val()== null)
                {

                    $("#possesion_status").parent().children('.error').css("display", "block");
                    $("#possesion_status").parent().children('.error').text("Please select Possession Status ");
                  isValid = false;
               }else{

                    $("#possesion_status").parent().children('.error').css("display", "none");
                isValid =  true;
               }
               return isValid;

        }

        function check_comp_date(){
        var isValid = false;
        if($("#possesion_status option:selected").text()=='Under Construction' ){

                if($("#date_of_delivery").val()=="" || $("#date_of_delivery").val()== null){
                  $("#ddelivery").parent().children('.error').css("display", "block");
                    $("#ddelivery").parent().children('.error').text("Please select Delivery Date ");
                  isValid = false;
                 }else{
                 $("#ddelivery").parent().children('.error').css("display", "none");
                 isValid = true;
                 }

        }else{

                    $("#ddelivery").parent().children('.error').css("display", "none");
                isValid =  true;
               }
               return isValid;

        }

		function chek_amenity(){
			var checkboxValues1 = []
			//var isValid = false;
			checkboxValues1 = $('.amenity:checked').map(function() {
			    return $(this).val();
			}).get();
			//alert(checkboxValues1.length);
			if (checkboxValues1.length == 0){
				$(".amenity_check").parent().children('.error').css("display", "block");
				$(".amenity_check").parent().children('.error').text("Please select atleast 1 Amenity");
				//isValid = false;
			   return false;
			}else{
				$(".amenity_check").parent().children('.error').css("display", "none");
				return true;
			}
		}

				function check_ex_am(extra_ame){
					var isValid = false;

					 $('.extra_ame').each(function( index ) {
						if($(this).val()=="")
			   	{
			     	$(this).parent().children('.error').css("display", "none");
			 //   	$(this).parent().children('.error').text("Please enter Shopping Mall/Market");
					isValid = true;
			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid Amenity");
					isValid = false;
			   }
			   else{
			   	$(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			  });
 			return isValid;
		}


		function check_ner(near_by_attr){
					var isValid = false;

					 $('.near_by_attr').each(function( index ) {
						if($(this).val()=="")
			   	{
			     	$(this).parent().children('.error').css("display", "none");
			 //   	$(this).parent().children('.error').text("Please enter Shopping Mall/Market");
					isValid = true;
			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid Amenity");
					isValid = false;
			   }
			   else{
			   	$(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			  });
 			return isValid;
		}

		function checkNearShoping(near_shop_mal){

				var isValid = false;

		   $('.near_shop_mal').each(function( index ) {

				if(index==0){

				  if($(this).val()=="")
			   {
			     	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter Shopping Mall/Market");
					isValid = false;
			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid Shopping Mall/Market");
					isValid = false;
			   }
			   else{
			   	$(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			}
			 else{
			 		if($(this).val()=="")
			   	{
			     	$(this).parent().children('.error').css("display", "none");
			 //   	$(this).parent().children('.error').text("Please enter Shopping Mall/Market");
					isValid = true;
			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid Shopping Mall/Market");
					isValid = false;
			   }
			   else{
			   	$(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }

			   }
				});
			  return isValid;
			}

		function checkNearShopingD(near_shop_d){
				var isValid = false;

			 $('.near_shop_d').each(function( index ) {
			   if(index==0){
				  if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter Distance");
					isValid = false;
			   }else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			 }else{
			 	if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "none");
			    //	$(this).parent().children('.error').text("Please enter Distance");
					isValid = true;
			   }else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }

			 }
				});

			   return isValid;
			}

	  function checkNearSchool(ner_sch){
	  			var isValid = false;

			   $('.ner_sch').each(function( index ) {
			   if(index==0){
				  if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter School Name");
					isValid = false;

			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid School Name");
					isValid = false;
			   }
			   else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			  }else{
			   if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "none");
			    //	$(this).parent().children('.error').text("Please enter School Name");
					isValid = true;

			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid School Name");
					isValid = false;
			   }
			   else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }


			  }
				});
				return isValid;

			}

		function checkNearSchoold(ner_schd){
				var isValid = false;
			   $('.ner_schd').each(function( index ) {
			   if(index==0){
				   if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter Distance");
					isValid = false;

			   }else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			   }else{
			   	   if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "none");
			    //	$(this).parent().children('.error').text("Please enter Distance");
					isValid = true;

			   }else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }

			   }
				});
				return isValid;

			}

			function checkNearHospital(ner_hos){
				var isValid = false;
			   $('.ner_hos').each(function( index ) {
			   if(index==0){
			    if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter Hospital");
					isValid = false;

			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid Hospital");
					isValid = false;
			   }
			   else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			 } else{
			 		if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "none");
			   // 	$(this).parent().children('.error').text("Please enter Hospital");
					isValid = true;

			   }else if($.isNumeric($(this).val())){
			   	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter valid Hospital");
					isValid = false;
			   }
			   else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }

			   }
				});
				return isValid;

			}

			function checkNearHospitald(ner_hosd){
				var isValid = false;
			   $('.ner_hosd').each(function( index ) {
			   if(index==0){
				 if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "block");
			    	$(this).parent().children('.error').text("Please enter Distance");
					isValid = false;

			   }else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }
			   }else{
			    if($(this).val()=='')
			   {
			    	$(this).parent().children('.error').css("display", "none");
			    //	$(this).parent().children('.error').text("Please enter Distance");
					isValid = true;

			   }else{
			    $(this).parent().children('.error').css("display", "none");
			   	isValid = true;
			   }

			   }
				});
			   return isValid;
			}

			  function railwaystation(){
			  var isValid = false;
			if($("#dis_rail_stat").val() =="")
			{
			    $("#dis_rail_stat").parent().children('.error').css("display", "block");
			    $("#dis_rail_stat").parent().children('.error').text("Please enter Distance");

			   isValid = false;
			   }else{
			    		    $("#dis_rail_stat").parent().children('.error').css("display", "none");
			  isValid = true;
			   }
			 return isValid;
		}

 		 function airport(){
 		   var isValid = false;
				if($("#dis_airport").val() =="")
				{

					$("#dis_airport").parent().children('.error').css("display", "block");
			    	$("#dis_airport").parent().children('.error').text("Please enter Distance");
				  isValid = false;
			   }else{

					$("#dis_airport").parent().children('.error').css("display", "none");
			   	isValid =  true;
			   }
			   return isValid;
		}

		function validspeciality(){

				var isValid = false;
				if($("#speciality").val() =="")
				{

					$("#speciality").parent().children('.error').css("display", "block");
			    	$("#speciality").parent().children('.error').text("Please enter Speciality");
				  isValid = false;
			   }else{

					$("#speciality").parent().children('.error').css("display", "none");
			   	isValid =  true;
			   }
			   return isValid;
		}





		function validateData(){
			if(checkCateg("#categ") & checkAdverttitle("#advert_title") & checkWebsite("#website")  & checkShortDesc('#short_discription') & checkProductName('.product_name_cls') & checkProductPrice('.product_price_cls') & checkPhoneCateg('.phone_type') & checkPhoneNumber('.phone_number') & checkEmail('#email_primary') & checkSecEmail('#email_secondary') & checkaddress('#address_line1') & checkArea('#area') & checkLandmark('#landmark')
			       & checkState("#statec") &  checkCity("#city") & checkPincode("#pincode") )
			{
					return true;
			}
				return false;
		}

		function validateproperty(){

			if(check_market_rate() & check_poss_status() & check_comp_date() &chek_amenity()& check_ex_am('.extra_ame') & check_ner('.near_by_attr') &  checkNearShoping('.near_shop_mal') & checkNearShopingD('.near_shop_d')  & checkNearSchool('.ner_sch') & checkNearSchoold('.ner_schd') & checkNearHospital('.ner_hos') & checkNearHospitald('.ner_hosd') & railwaystation() & airport()){
				return true;
			}
			else{
				return false;
			}
		}


		$("#save-advert").click(function(event)  {
		  event.preventDefault();

            advert_keywords = $("#advert_keywords").val();
            advert_keywords = $('#advert_keywords').val().split(",");
            var a = advert_keywords.length;

            if (a > 75) {
                $('#error-message1').text('Maximum limit for keywords is 75');
                $('#error-modal1').modal('show');
                return false;
            }

			var file_size_check	= checkFileSize();

		  	if(file_size_check == false){
		  			return false;
		  	}


});




$("#save").click(function(event)  {
	$("#success-modal").modal('hide');
				user_id = "{{user_id}}"



			 var formData= new FormData();
			var check_image = 0;

				var display_image = document.getElementById("display_image");
	         display_image = display_image.files[0];

	         if (display_image == undefined) {
	                display_image = "";
	          }
	         else {
	          check_image = 1;
	          formData.append("display_image", display_image);
	      }

	      	var product_name_list = []
			product_name_list = $('.product_name_cls').map(function() {

			    return $(this).val();
			}).get();

				var product_price_list = []
			product_price_list = $('.product_price_cls').map(function() {

			    return $(this).val();
			}).get();

			var phone_category_list = []
			phone_category_list = $('.phone_type').map(function() {

			    return $(this).val();
			}).get();


			var phone_number_list = []
			phone_number_list = $('.phone_number').map(function() {
			    return $(this).val();
			}).get();

			var opening_day_list = []
			opening_day_list = $('.opening_day').map(function() {
			    return $(this).val();
			}).get();


			var start_time_list = []
			start_time_list = $('.time_start').map(function() {
			    return $(this).val();

			}).get();


			var abc=start_time_list;
    		var str = abc.toString();


			res = str.replace(/^[,]+|[,]+$|[,]+/g,",").trim();
			while(res.charAt(0) === ',')
  				  res = res.substr(1);


			var end_time_list = []
			end_time_list = $('.time_end').map(function() {
			    return $(this).val();
			}).get();

			var pqr = end_time_list;
			var str1 = pqr.toString();


			res1 = str1.replace(/^[,]+|[,]+$|[,]+/g,",").trim();
			while(res1.charAt(0) === ',')
  				  res1 = res1.substr(1);


			var checkboxValues = []
			checkboxValues = $('.amenity:checked').map(function() {
			    return $(this).val();
			}).get();

			var exe_ame = []
			exe_ame = $('.extra_ame').map(function() {
			    return $(this).val();
			}).get();

			var near_attr = []
			near_attr = $('.near_by_attr').map(function() {
			    return $(this).val();
			}).get();

			var near_shomal = []
			near_shomal = $('.near_shop_mal').map(function() {
			    return $(this).val();
			}).get();

			var near_shomald = []
			near_shomald = $('.near_shop_d').map(function() {
			    return $(this).val();
			}).get();

			var near_schol = []
			near_schol = $('.ner_sch').map(function() {
			    return $(this).val();
			}).get();

			var near_schold = []
			near_schold = $('.ner_schd').map(function() {
			    return $(this).val();
			}).get();

			var near_hosp = []
			near_hosp = $('.ner_hos').map(function() {
			    return $(this).val();
			}).get();

			var near_hospd = []
			near_hospd = $('.ner_hosd').map(function() {
			    return $(this).val();
			}).get();


		  event.preventDefault();

		  var file_size_check	= checkFileSize();

		  	if(file_size_check == false){
		  			return false;
		  	}

			if(validateData()){

			if($('#categ option:selected').text()== "Restaurants" || $('#categ option:selected').text()== "Health" ||
    		$('#categ option:selected').text()== "Lifestyle" || $('#categ  option:selected').text()== "Travel" || $('#categ  option:selected').text()== "Electronics"
    		){

    			 isValid = false;
				var check_speciality = validspeciality();
				if (check_speciality == false){

					return false;
				}

    		}


			if($("#categ option:selected").text() == "Real Estate"){
			 isValid = false;
				var asd = validateproperty();
				if (asd == false){

					return false;
				}

				}

     $.each($(".subcat_select"), function(){
 		var subcat_name = $(this).find(":selected").val();
		if(subcat_name){subcat_list.push(subcat_name);
		}
       })

        advert_keywords = $("#advert_keywords").val();


		formData.append("user_id",$('#user_id').val());
		formData.append("subscription_id",$('#subscription_id').val());
		formData.append("lat",$('#lat').val());
		formData.append("lng",$('#lng').val());
		formData.append("categ",$('#categ').val());
		formData.append("subcat_list",subcat_list);
        formData.append("advert_keywords",advert_keywords);
		formData.append("advert_title",$('#advert_title').val());
		formData.append("website",$('#website').val());
		formData.append("short_discription",$('#short_discription').val());
		formData.append("product_discription",$('#product_discription').val());
		formData.append("discount_discription",$('#discount_discription').val());
		formData.append("currency",$('#currency').val());
		formData.append("email_primary",$('#email_primary').val());
		formData.append("email_secondary",$('#email_secondary').val());
		formData.append("address_line1",$('#address_line1').val());
		formData.append("address_line2",$('#address_line2').val());
		formData.append("area",$('#area').val());
		formData.append("landmark",$('#landmark').val());
		formData.append("statec",$('#statec').val());
		formData.append("city",$('#city').val());
		formData.append("pincode",$('#pincode').val());
		formData.append("opening_day_list",opening_day_list);
		formData.append("start_time_list",res);
		formData.append("end_time_list",res1);
		formData.append("any_other_details",$('#any_other_details').val());
		formData.append("ac_attachment",$('#ac_attachments').val());
		formData.append("attachments",$('#attachment').val());
		formData.append("phone_category_list",phone_category_list);
		formData.append("phone_number_list",phone_number_list);
	   formData.append("phone_list",$('#categ').val());
		formData.append("check_image",check_image);
		formData.append("pro_mark_rate",$('#pro_mark_rate').val());
		formData.append("possesion_status",$('#possesion_status').val());
		formData.append("date_of_delivery",$('#date_of_delivery').val());
        formData.append("other_projects",$('#other_projects').val());
		formData.append("amenity_list",checkboxValues);
		formData.append("additional_amenity",exe_ame);
		formData.append("near_attraction",near_attr);
		formData.append("near_shopnmal",near_shomal);
		formData.append("near_shonmald",near_shomald);
		formData.append("near_schol",near_schol);
		formData.append("near_schold",near_schold);
	   formData.append("near_hosp",near_hosp);
		formData.append("near_hospd",near_hospd);
		formData.append("dis_rail_stat",$('#dis_rail_stat').val());
		formData.append("dis_airport",$('#dis_airport').val());
		formData.append("happy_hour_offer",$('#happy_hour_offer').val());
		formData.append("facility",$('#facility').val());
		formData.append("course_duration",$('#course_duration').val());
		formData.append("affilated",$('#affilated').val());
		formData.append("speciality",$('#speciality').val());
		formData.append("product_name_list",product_name_list);
		formData.append("product_price_list",product_price_list);
		formData.append("image_and_video_space",$('#image_and_video_space').val());




  			$.ajax({

				  type	: "POST",
				   url : '/save-advert/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
	              		$("#affiliate-modal").modal('show');

	              	}
	      			if (response.success == "false") {
							$("#error-modal").modal('show');
	       			}
               },
                 beforeSend: function () {

                $("#processing").css('display','block');

            },
            complete: function () {
                $("#processing").css('display','none');
            },
               error : function(response){
                  	alert("_Error");
            	}
           });
  }
});

$("#continue").click(function(event)  {
	$("#success-modal").modal('hide');
 $("#form_wizard_1").bootstrapWizard('show',1);
});


function activate_service(){
	$("#success-modal1").modal('hide');
 $("#form_wizard_1").bootstrapWizard('show',1);
}





	 			//Validation End-----------------------------//<label class="error" style="color:red; display:none;"></label>





            $("#statec").change(function () {
					getCity();
				});
				$("#city").change(function () {
					getPincode();
				});


        $('.property_status').change(function () {

    		 if($('.property_status').val()=="Under Construction"){
    		$("#dateofdelivery").show();
    		}
    		else{
    		$("#dateofdelivery").hide();
    		}
		});


			var totalSizeLimit = 1*1024*1024; //300MB
			var dropzone3;





              //init start timepicker
                    var start = $("#start"+i).kendoTimePicker({
                        change: startChange
                    }).data("kendoTimePicker");

                    //init end timepicker
                    var end = $("#end"+i).kendoTimePicker().data("kendoTimePicker");

                    //define min/max range
                    start.min("8:00 AM");
                    start.max("6:00 PM");

                    //define min/max range
                    end.min("8:00 AM");
                    end.max("7:30 AM");

						function startChange() {
                        var startTime = start.value();

                        if (startTime) {
                            startTime = new Date(startTime);

                            end.max(startTime);

                            startTime.setMinutes(startTime.getMinutes() + this.options.interval);

                            end.min(startTime);
                            end.value(startTime);
                        }
                    }



          });



    //---------------------------------------validation for number----------------//


    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57 || charCode == 43 || charCode == 45 ))
            return false;
        return true;
    }

    function validateFloatKeyPresss(el, evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode;
        var number = el.value.split('+');
        var number1 = el.value.split('-');
        if (charCode != 45 && charCode != 43 && charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        //just one dot
        if (number.length > 1 && charCode == 43) {
            return false;
        }
        if (number1.length > 1 && charCode == 45) {
            return false;
        }
        return true;
    }


function clear_subcat(){
    for(i=1;i<=5;i++){
        $('#lvl'+i+'_row').hide();
        $('#lvl'+i).removeAttr('required');
    }
}

function check_cat(lvl,this_val){
    if($(this_val).attr('data-level')=="0"){
    clear_subcat();
    }
    $.ajax({
        type	: "POST",
        url : '/check-category/',
        data : {'category_id':$(this_val).val(),'cat_level':lvl},
        success: function (response) {
            if(response.success!='false'){
                $('#lvl'+lvl).html('');
                $('.subcat_select').select2();
                $('.select2').css("width","100%");
                $('#lvl'+lvl).append('<option value="">Select SubCategory</option>');
                $.each(response.category_list, function (index, item) {
                    $('#lvl'+lvl).append(item);
                });
                for(i=1;i<=lvl;i++){
                    $('#lvl'+i+'_row').show();
                }
                $('#lvl'+lvl).attr('required','required');
            }
        },
        error : function(response){
            alert("_Error");
        }
    });
}

