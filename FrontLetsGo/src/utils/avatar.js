/**
 * Utilitaire pour la gestion des avatars utilisateur
 * Règle : Toujours privilégier la vraie photo uploadée par l'utilisateur.
 * Si aucune photo n'est fournie, génère un avatar personnalisé par défaut (initiales ou icône moderne),
 * et JAMAIS une photo générique pré-générée d'un tiers.
 */

export function getInitials(nameOrFirst, maybeLast) {
  // Cas 1 : Deux arguments distincts passés explicitement (ex: prenom, nom)
  if (maybeLast !== undefined && maybeLast !== null && typeof maybeLast === 'string' && maybeLast.trim()) {
    const firstInitial = (typeof nameOrFirst === 'string' && nameOrFirst.trim()) ? nameOrFirst.trim()[0] : ''
    const lastInitial = maybeLast.trim()[0]
    if (firstInitial && lastInitial) {
      return (firstInitial + lastInitial).toUpperCase()
    }
    if (firstInitial) return firstInitial.toUpperCase()
    if (lastInitial) return lastInitial.toUpperCase()
  }

  // Cas 2 : Objet utilisateur passé en paramètre
  if (nameOrFirst && typeof nameOrFirst === 'object') {
    const p = (nameOrFirst.prenom || nameOrFirst.firstName || nameOrFirst.first_name || '').trim()
    const n = (nameOrFirst.nom || nameOrFirst.lastName || nameOrFirst.last_name || '').trim()
    if (p && n) {
      return (p[0] + n[0]).toUpperCase()
    }
    const alternatif = (nameOrFirst.nomComplet || nameOrFirst.name || p || n || '').trim()
    return getInitials(alternatif)
  }

  if (!nameOrFirst || typeof nameOrFirst !== 'string') return ''

  // Cas 3 : Chaîne complète "Prénom Nom"
  const parts = nameOrFirst.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return ''
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  }

  // Cas 4 : Un seul mot ou deux initiales directes (ex: "MD")
  if (parts[0].length === 2 && /^[A-Za-z]{2}$/.test(parts[0])) {
    return parts[0].toUpperCase()
  }

  // Si un seul prénom sans nom est disponible, renvoyer son initiale unique
  return parts[0][0].toUpperCase()
}

export function generateInitialsAvatar(initials, bgColor = '#FF4D2D', textColor = '#FFFFFF') {
  const safeInitials = initials ? initials.slice(0, 2).toUpperCase() : 'LG'
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
    <rect width="100" height="100" rx="50" fill="${bgColor}"/>
    <text x="50" y="55" font-family="'Plus Jakarta Sans', system-ui, -apple-system, sans-serif" font-size="38" font-weight="700" fill="${textColor}" text-anchor="middle" dominant-baseline="middle" letter-spacing="1">
      ${safeInitials}
    </text>
  </svg>`
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
}

export function getDefaultAvatar(nameOrInitials, maybeLast = '') {
  const initials = getInitials(nameOrInitials, maybeLast)
  return generateInitialsAvatar(initials)
}

export function getAvatarUrl(photoUrl, fullNameOrFirst = '', maybeLast = '') {
  // Ignorer les anciens profils mockés ou génériques
  if (!photoUrl || photoUrl.includes('avatar_thomas') || photoUrl.trim() === '') {
    return getDefaultAvatar(fullNameOrFirst, maybeLast)
  }

  // Si c'est déjà un data URL, blob ou URL absolue
  if (photoUrl.startsWith('data:') || photoUrl.startsWith('blob:') || photoUrl.startsWith('http://') || photoUrl.startsWith('https://')) {
    return photoUrl
  }

  // Si c'est un chemin relatif renvoyé par Django (ex: /media/photos_profil/...)
  if (photoUrl.startsWith('/media/')) {
    return `http://127.0.0.1:8000${photoUrl}`
  }

  return photoUrl
}
