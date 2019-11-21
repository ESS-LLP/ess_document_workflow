import frappe

@frappe.whitelist()
def get_appointment_workflow(appointment):
	appointment_doc = frappe.get_doc("Patient Appointment", appointment)
	workflow_list = []
	if appointment_doc.appointment_type:
		appointment_type = frappe.get_doc("Appointment Type", appointment_doc.appointment_type)
		if appointment_type.nav_appointment_workflow:
			for workflow in appointment_type.nav_appointment_workflow:
				workflow_doctype = doc_for_appoitnment(workflow.workflow_doctype, appointment)
				if workflow_doctype:
					workflow_list.append(workflow_doctype.as_dict())
				else:
					workflow_doctype = {"new_doc": True, "appointment": appointment,
						"patient": appointment_doc.patient, "doctype": workflow.workflow_doctype}
					workflow_list.append(workflow_doctype)
	return workflow_list

def doc_for_appoitnment(dt_from_appointment, appointment):
	dn_from_appointment = frappe.db.exists(
		dt_from_appointment,
		{
			"appointment": appointment
		}
	)
	if dn_from_appointment:
		return frappe.get_doc(dt_from_appointment, dn_from_appointment)
	return False
