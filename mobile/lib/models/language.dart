class Language {
  const Language({
    this.publicId,
    required this.name,
    required this.code,
  });

  final String? publicId;
  final String name;
  final String code;

  factory Language.fromJson(Map<String, dynamic> json) {
    return Language(
      publicId: json['public_id'] as String?,
      name: json['language_name'] as String,
      code: json['language_code'] as String,
    );
  }
}
