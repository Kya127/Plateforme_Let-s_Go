from django.contrib import admin
from .models import User, VerificationDocument

@admin.register(VerificationDocument)
class VerificationDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fields = (
        'user', 
        'status', 
        'permis_conduire', 
        'carte_grise', 
        'assurance', 
        'photo_vehicule',
        'motif_rejet', 
        'created_at', 
        'updated_at'
    )

    def save_model(self, request, obj, form, change):
        """
        Déclenché lorsque l'admin clique sur 'Enregistrer' dans la fiche d'un document.
        """
        # Si l'admin valide le dossier
        if obj.status == VerificationDocument.Status.APPROUVE:
            obj.motif_rejet = ""  # Reinitialiser le motif s'il y en avait un
            obj.user.role = User.Role.CONDUCTEUR
            obj.user.is_verified = True
            obj.user.save()

        # Si l'admin rejette le dossier
        elif obj.status == VerificationDocument.Status.REJETE:
            obj.user.is_verified = False
            obj.user.save()

        super().save_model(request, obj, form, change)