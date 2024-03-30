from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from django.db.models import Q


class Identify(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        phoneNumber = request.data.get("phoneNumber")
        try:
            if email and phoneNumber:
                data = {
                        "contact": {
                            "primaryContatctId": None,
                            "emails": [],
                            "phoneNumbers": [],
                            "secondaryContactIds": []
                            }
                        }
                exact_contact = Contact.objects.filter(Q(email=email) &
                                                       Q(phoneNumber=phoneNumber))
                similar_contacts = Contact.objects.filter(
                                                        Q(email=email) |
                                                        Q(phoneNumber=phoneNumber)).exclude(
                                                        email=email, phoneNumber=phoneNumber)
                if len(exact_contact) != 0:
                    if exact_contact.first().linkPrecedence == "primary":
                        data["contact"]["primaryContatctId"] = exact_contact.first().id
                    else:
                        data["contact"]["secondaryContactIds"].append(exact_contact.first().id)
                    data["contact"]["emails"].append(exact_contact.first().email)
                    data["contact"]["phoneNumbers"].append(exact_contact.first().phoneNumber)
                    for contact in similar_contacts:
                        if contact.linkPrecedence == "primary":
                            data["contact"]["primaryContatctId"] = contact.id
                        else:
                            data["contact"]["secondaryContactIds"].append(
                                contact.id)
                        data["contact"]["emails"].append(contact.email)
                        data["contact"]["phoneNumbers"].append(contact.phoneNumber)
                elif len(similar_contacts) != 0:
                    primary_contacts = similar_contacts.filter(linkPrecedence="primary")
                    if len(primary_contacts) == 1:
                        new_contact = Contact.objects.create(email=email,
                                                             phoneNumber=phoneNumber,
                                                             linkPrecedence="secondary",
                                                             linkedId=primary_contacts.first().id
                                                             )
                        data["contact"]["primaryContatctId"] = primary_contacts.first().id
                        data["contact"]["emails"].append(new_contact.email)
                        data["contact"]["phoneNumbers"].append(new_contact.phoneNumber)
                        data["contact"]["emails"].append(primary_contacts.first().email)
                        data["contact"]["phoneNumbers"].append(primary_contacts.first().phoneNumber)
                        data["contact"]["secondaryContactIds"].append(new_contact.id)
                        for contact in similar_contacts.difference(primary_contacts):
                            data["contact"]["emails"].append(contact.email)
                            data["contact"]["phoneNumbers"].append(contact.phoneNumber)
                            data["contact"]["secondaryContactIds"].append(contact.id)
                    elif len(primary_contacts) > 1:
                        primary_contacts.order_by("createdAt")
                        data["contact"]["primaryContatctId"] = primary_contacts.first().id
                        data["contact"]["emails"].append(primary_contacts.first().email)
                        data["contact"]["phoneNumbers"].append(
                            primary_contacts.first().phoneNumber)
                        for contact in primary_contacts[1:]:
                            contact.linkedId = primary_contacts.first().id
                            contact.linkPrecedence = "secondary"
                            contact.save()
                            data["contact"]["emails"].append(contact.email)
                            data["contact"]["phoneNumbers"].append(contact.phoneNumber)
                            data["contact"]["secondaryContactIds"].append(contact.id)
                        for contact in similar_contacts:
                            if contact not in primary_contacts:
                                data["contact"]["emails"].append(contact.email)
                                data["contact"]["phoneNumbers"].append(contact.phoneNumber)
                                data["contact"]["secondaryContactIds"].append(contact.id)
                    else:
                        new_contact = Contact.objects.create(email=email,
                                                             phoneNumber=phoneNumber,
                                                             linkPrecedence="primary")
                        data["contact"]["primaryContatctId"] = new_contact.id
                        data["contact"]["emails"].append(new_contact.email)
                        data["contact"]["phoneNumbers"].append(new_contact.phoneNumber)
                        for contact in similar_contacts.difference(primary_contacts):
                            data["contact"]["emails"].append(contact.email)
                            data["contact"]["phoneNumbers"].append(
                                contact.phoneNumber)
                            data["contact"]["secondaryContactIds"].append(
                                contact.id)
                else:
                    new_contact = Contact.objects.create(email=email,
                                                         phoneNumber=phoneNumber,
                                                         linkPrecedence="primary")
                    data["contact"]["primaryContatctId"] = new_contact.id
                    data["contact"]["emails"].append(new_contact.email)
                    data["contact"]["phoneNumbers"].append(new_contact.phoneNumber)
                data["contact"]["emails"] = list(set(data["contact"]["emails"]))
                data["contact"]["phoneNumbers"] = list(set(data["contact"]["phoneNumbers"]))
                data["contact"]["secondaryContactIds"] = list(set(
                                                              data["contact"]["secondaryContactIds"]
                                                              ))
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                        "message": "email and phoneNumber both can't null in payload."
                    }
                return Response(data=data, status=status.HTTP_200_OK)

        except Exception as error:
            data = {"message": str(error)}
            return Response(data=data, status=status.HTTP_200_OK)
