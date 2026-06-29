class Difficulty {
  const Difficulty({
    this.publicId,
    required this.name,
  });

  final String? publicId;
  final String name;

  factory Difficulty.fromJson(Map<String, dynamic> json) {
    return Difficulty(
      publicId: json['public_id'] as String?,
      name: json['difficulty'] as String,
    );
  }
}
