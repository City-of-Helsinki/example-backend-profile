from helsinki_gdpr.types import Error, ErrorResponse, LocalizedMessage


def delete_gdpr_data(user_data, dry_run):
    # If the pet_name is "nodelete" this will indicate that the user can't
    # be deleted as to help testing the GDRP delete functionality.
    if user_data.pet_name == "nodelete":
        return ErrorResponse(
            [
                Error(
                    "PET_MUST_SURVIVE",
                    {
                        "en": "Pet must survive",
                        "fi": "Lemmikin täytyy selvitä",
                        "sv": "Husdjuret måste överleva",
                    },
                )
            ]
        )

    # Delete user's User instance.
    # The deletion cascades to the UserData instance as well.
    user_data.user.delete()
