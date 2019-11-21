## Document Workflow

Navigate DocType based on document workflow

## Set Workflow by adding Custom Script in doctype
frappe.ui.form.on("doctype",{ // script for this doctype
	refresh:  function(frm){
		frappe.call({
			method:"ess_document_workflow.document_workflow.utils.get_appointment_workflow",
			args: {appointment: frm.doc.appointment_field}, // appointment_field in the doctype
			callback: function(data){
				if(!data.exc){
					var workflow_list = data.message;
					workflow_list.forEach(function(workflow_doctype, i) {
						if(frm.doc.doctype != workflow_doctype.doctype){
							frm.add_custom_button(__(workflow_doctype.doctype), function() {
								if (!("new_doc" in workflow_doctype)){
									var doclist = frappe.model.sync(workflow_doctype);
									frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
								}
								else{
									frappe.route_options = {
										"appointment": workflow_doctype.appointment,
										"patient": workflow_doctype.patient
									};
									frappe.new_doc(workflow_doctype.doctype);
								}
							},__("Workflow"));
						}
					});
					if(frm.doc.doctype != "Patient Appointment") {
						frm.add_custom_button(__("Patient Appointment"), function() {
							frappe.set_route("Form", "Patient Appointment", frm.doc.appointment);
						},__("Workflow"));
					}
				}
			}
		});
	}
});

#### License

MIT
