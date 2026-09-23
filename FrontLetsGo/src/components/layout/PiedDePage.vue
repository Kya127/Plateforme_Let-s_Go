<script setup>
</script>

<template>
  <footer class="pied-de-page">
    <div class="conteneur-footer">
      <!-- En-tête du Footer avec Logo, Slogan & Réseaux Sociaux -->
      <div class="footer-haut">
        <div class="footer-marque">
          <h2 class="footer-logo">
            <span class="texte-blanc">LET'S </span><span class="texte-orange">GO</span>
          </h2>
          <p class="footer-slogan">La plateforme de covoiturage de référence au Sénégal.</p>
          <span class="slogan-wolof-footer">« Yoon wi ñou bolee ! »</span>
        </div>

        <div class="footer-reassurance">
          <div class="reassurance-item">
            <span class="reassurance-icone">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                <polyline points="9 12 11 14 15 10" />
              </svg>
            </span>
            <div>
              <strong class="reassurance-titre">100% Vérifié</strong>
              <p class="reassurance-texte">Permis et carte grise contrôlés</p>
            </div>
          </div>
          <div class="reassurance-item">
            <span class="reassurance-icone">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="4" width="20" height="16" rx="3" />
                <circle cx="16" cy="12" r="2" fill="#FF4D2D" />
                <path d="M2 10h20" />
              </svg>
            </span>
            <div>
              <strong class="reassurance-titre">Économique</strong>
              <p class="reassurance-texte">Partage équitable des frais de route</p>
            </div>
          </div>
        </div>
      </div>

      <div class="separateur-footer"></div>

      <!-- Grille des liens + Réseaux Sociaux -->
      <div class="grille-liens">
        <!-- Colonne 1 -->
        <div class="colonne-liens">
          <h4 class="colonne-titre">Navigation</h4>
          <ul class="liste-liens">
            <li><router-link to="/accueil">Accueil</router-link></li>
            <li><router-link to="/accueil">Rechercher un trajet</router-link></li>
            <li><router-link to="/connexion?redirection=/conducteur/tableau-de-bord">Publier un trajet</router-link></li>
            <li><router-link to="/onboarding">Comment ça marche</router-link></li>
          </ul>
        </div>

        <!-- Colonne 2 -->
        <div class="colonne-liens">
          <h4 class="colonne-titre">Conducteurs</h4>
          <ul class="liste-liens">
            <li><router-link to="/connexion?redirection=/conducteur/tableau-de-bord">Espace conducteur</router-link></li>
            <li><a href="#charte">Vérification documentaire</a></li>
            <li><a href="#assurance">Assurances & Sécurité</a></li>
            <li><a href="#frais">Estimation des économies</a></li>
          </ul>
        </div>

        <!-- Colonne 3 -->
        <div class="colonne-liens">
          <h4 class="colonne-titre">Trajets Populaires</h4>
          <ul class="liste-liens">
            <li><a href="#trajet">Dakar ➔ Thiès</a></li>
            <li><a href="#trajet">Dakar ➔ Saint-Louis</a></li>
            <li><a href="#trajet">Dakar ➔ Touba</a></li>
            <li><a href="#trajet">Mbour ➔ Dakar</a></li>
          </ul>
        </div>

        <!-- Colonne 4 : Réseaux Sociaux & Contact -->
        <div class="colonne-liens colonne-reseaux">
          <h4 class="colonne-titre">Rejoignez-nous</h4>
          <p class="reseaux-descriptif">Suivez l'actualité de la communauté Let's Go partout au Sénégal :</p>
          
          <div class="liste-icones-sociales">
            <!-- Facebook -->
            <a href="https://facebook.com" target="_blank" rel="noopener" class="lien-social" aria-label="Facebook">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>

            <!-- X / Twitter -->
            <a href="https://twitter.com" target="_blank" rel="noopener" class="lien-social" aria-label="X (Twitter)">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>

            <!-- Instagram -->
            <a href="https://instagram.com" target="_blank" rel="noopener" class="lien-social" aria-label="Instagram">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
              </svg>
            </a>

            <!-- LinkedIn -->
            <a href="https://linkedin.com" target="_blank" rel="noopener" class="lien-social" aria-label="LinkedIn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
              </svg>
            </a>

            <!-- WhatsApp -->
            <a href="https://wa.me/221770000000" target="_blank" rel="noopener" class="lien-social lien-whatsapp" aria-label="WhatsApp">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
              </svg>
            </a>
          </div>

          <p class="contact-direct">
            <strong>Support :</strong> support@letsgo.sn<br />
            <strong>Téléphone :</strong> +221 33 800 00 00
          </p>
        </div>
      </div>

      <div class="separateur-footer"></div>

      <!-- Bas du footer avec Copyright -->
      <div class="footer-bas">
        <p class="copyright-texte">
          © 2026 LET'S GO CARPOOLING SÉNÉGAL — TOUS DROITS RÉSERVÉS.
        </p>
        <div class="footer-bas-droite">
          <span class="badge-pays">
            <svg width="18" height="12" viewBox="0 0 18 12" class="drapeau-svg" style="border-radius: 2px; display: inline-block; vertical-align: middle; margin-right: 6px;">
              <rect width="6" height="12" fill="#00853F" />
              <rect x="6" width="6" height="12" fill="#FDEF42" />
              <rect x="12" width="6" height="12" fill="#E31B23" />
              <polygon points="9,3.8 9.8,6.2 7.8,4.7 10.2,4.7 8.2,6.2" fill="#00853F" />
            </svg>
            Sénégal
          </span>
          <span class="texte-certifie">Plateforme de covoiturage certifiée</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.pied-de-page {
  background-color: #111627;
  color: #E5E7EB;
  padding: 56px 24px 32px;
  width: 100%;
  margin-top: 48px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.conteneur-footer {
  max-width: 1140px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.footer-haut {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 28px;
}

.footer-logo {
  font-family: var(--font-family-base);
  font-size: 32px;
  font-weight: 900;
  letter-spacing: -0.5px;
  margin-bottom: 6px;
}

.texte-blanc {
  color: var(--color-white);
}

.texte-orange {
  color: var(--color-brand-accent);
}

.footer-slogan {
  font-size: 14.5px;
  color: #9CA3AF;
  margin-bottom: 4px;
}

.slogan-wolof-footer {
  font-size: 13.5px;
  font-style: italic;
  color: #FFE6D5;
}

.footer-reassurance {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reassurance-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.04);
  padding: 12px 16px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.reassurance-icone {
  font-size: 22px;
}

.reassurance-titre {
  display: block;
  font-size: 13px;
  color: var(--color-white);
}

.reassurance-texte {
  font-size: 12px;
  color: #9CA3AF;
}

.separateur-footer {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.08);
  margin: 20px 0 32px;
}

/* Grille */
.grille-liens {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px 24px;
}

.colonne-titre {
  font-family: var(--font-family-base);
  font-size: 13px;
  font-weight: 800;
  color: var(--color-white);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.liste-liens {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 11px;
}

.liste-liens a {
  color: #9CA3AF;
  font-size: 14px;
  transition: color var(--transition-fast);
}

.liste-liens a:hover {
  color: var(--color-brand-accent);
}

/* Réseaux sociaux */
.colonne-reseaux {
  grid-column: span 2;
}

.reseaux-descriptif {
  font-size: 13.5px;
  color: #9CA3AF;
  line-height: 1.5;
  margin-bottom: 14px;
}

.liste-icones-sociales {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.lien-social {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #D1D5DB;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.lien-social:hover {
  background-color: var(--color-brand-accent);
  color: var(--color-white);
  border-color: var(--color-brand-accent);
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(255, 77, 45, 0.35);
}

.lien-whatsapp:hover {
  background-color: #25D366;
  border-color: #25D366;
  box-shadow: 0 6px 14px rgba(37, 211, 102, 0.35);
}

.contact-direct {
  font-size: 13px;
  line-height: 1.7;
  color: #9CA3AF;
}

.contact-direct strong {
  color: var(--color-white);
}

/* Bas */
.footer-bas {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.copyright-texte {
  font-size: 12px;
  color: #6B7280;
  letter-spacing: 0.5px;
}

.footer-bas-droite {
  display: flex;
  align-items: center;
  gap: 12px;
}

.badge-pays {
  font-size: 12px;
  font-weight: 600;
  color: #E5E7EB;
  background: rgba(255, 255, 255, 0.08);
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.texte-certifie {
  font-size: 12px;
  color: #9CA3AF;
}

/* Adaptation Desktop */
@media (min-width: 768px) {
  .footer-haut {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .footer-reassurance {
    flex-direction: row;
  }

  .grille-liens {
    grid-template-columns: repeat(4, 1fr);
    gap: 32px;
  }

  .colonne-reseaux {
    grid-column: span 1;
  }

  .footer-bas {
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>
